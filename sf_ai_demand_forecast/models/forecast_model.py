# Config model defined in forecast_model.py
import json
import logging
import pickle
from datetime import timedelta

from odoo import api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)

try:
    import numpy as np
    from sklearn.ensemble import (GradientBoostingRegressor,
                                  RandomForestRegressor)
    from sklearn.linear_model import LinearRegression
    from sklearn.metrics import mean_absolute_error
    HAS_SKLEARN = True
except ImportError:  # pragma: no cover - handled at runtime with clear error
    HAS_SKLEARN = False


class ForecastModel(models.Model):
    _name = 'forecast.model'
    _description = 'Demand Forecast Model'
    _order = 'create_date desc'

    name = fields.Char(string='Model Name', required=True)
    algorithm = fields.Selection([
        ('gb', 'Gradient Boosting'),
        ('rf', 'Random Forest'),
        ('lr', 'Linear Regression'),
    ], string='Algorithm', default='gb', required=True)
    active = fields.Boolean(default=True)

    # Training scope
    product_ids = fields.Many2many(
        'product.product', string='Products',
        domain=[('type', 'in', ['product', 'consu'])])
    warehouse_ids = fields.Many2many('stock.warehouse', string='Warehouses')
    date_from = fields.Date(string='Training Data From')
    date_to = fields.Date(string='Training Data To')

    # Hyperparameters
    n_estimators = fields.Integer(string='N Estimators', default=100)
    max_depth = fields.Integer(string='Max Depth', default=6)
    learning_rate = fields.Float(string='Learning Rate', default=0.1)
    min_samples_split = fields.Integer(string='Min Samples Split', default=10)

    # Features
    use_lags = fields.Boolean(string='Use Lag Features', default=True)
    use_rolling = fields.Boolean(string='Use Rolling Stats', default=True)
    use_calendar = fields.Boolean(string='Use Calendar Features', default=True)

    # Training status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('training', 'Training'),
        ('trained', 'Trained'),
        ('failed', 'Failed'),
    ], string='Status', default='draft', readonly=True)

    # Metrics
    mae = fields.Float(string='MAE', readonly=True)
    mape = fields.Float(string='MAPE %', readonly=True)
    rmse = fields.Float(string='RMSE', readonly=True)
    bias = fields.Float(string='Bias', readonly=True)
    training_samples = fields.Integer(string='Training Samples', readonly=True)
    validation_samples = fields.Integer(string='Validation Samples',
                                        readonly=True)
    training_duration = fields.Float(string='Training Duration (s)',
                                     readonly=True)
    last_trained = fields.Datetime(string='Last Trained', readonly=True)
    error_message = fields.Text(string='Error', readonly=True)

    prediction_ids = fields.One2many('forecast.prediction', 'model_id',
                                     string='Predictions')
    training_log_ids = fields.One2many('forecast.training.log', 'model_id',
                                       string='Training Logs')
    model_attachment_id = fields.Many2one(
        'ir.attachment', string='Trained Model (pickle)', readonly=True)

    # ------------------------------------------------------------------ cron
    @api.model
    def cron_retrain(self):
        """Retrain active models whose retrain frequency elapsed."""
        today = fields.Date.today()
        freq_days = {'daily': 1, 'weekly': 7, 'monthly': 30}
        for cfg in self.env['forecast.config'].search([]):
            if not cfg.auto_retrain:
                continue
            days = freq_days.get(cfg.retrain_frequency, 7)
            models = self.search([('active', '=', True),
                                  ('state', 'in', ['draft', 'trained'])])
            for mdl in models:
                if mdl.last_trained and (
                        fields.Date.to_date(mdl.last_trained)
                        > today - timedelta(days=days)):
                    continue
                mdl.action_train()

    # --------------------------------------------------------------- actions
    def action_train(self):
        if not HAS_SKLEARN:
            raise UserError(_(
                'scikit-learn is not installed on this server. '
                'Install it with: pip install scikit-learn'))
        for model in self:
            model.state = 'training'
            model.error_message = False
            start_time = fields.Datetime.now()
            try:
                model._run_training(start_time)
                model.state = 'trained'
            except Exception as e:
                _logger.exception('Training failed')
                model.write({
                    'state': 'failed',
                    'error_message': str(e),
                    'training_duration':
                        (fields.Datetime.now() - start_time).total_seconds()
                        if start_time else 0.0,
                })
                self.env['forecast.training.log'].create({
                    'model_id': model.id,
                    'status': 'failed',
                    'message': str(e)[:500],
                })

    def action_generate_predictions(self):
        """(Re)generate the prediction horizon using the trained model."""
        if not HAS_SKLEARN:
            raise UserError(_('scikit-learn is not installed.'))
        for model in self.filtered(lambda m: m.state == 'trained'):
            model._generate_predictions()

    # ------------------------------------------------------------ data prep
    def _demand_domain(self):
        self.ensure_one()
        domain = [
            ('state', '=', 'done'),
            ('location_id.usage', '=', 'internal'),
            ('location_dest_id.usage', '=', 'customer'),
        ]
        if self.product_ids:
            domain.append(('product_id', 'in', self.product_ids.ids))
        return domain

    def _fetch_series(self):
        """Aggregate done customer shipments to daily demand rows.

        Returns dict[(product_id, warehouse_id)] -> {date: qty}.
        """
        self.ensure_one()
        StockMove = self.env['stock.move']
        domain = self._demand_domain()
        if self.date_from:
            domain.append(('date', '>=', self.date_from))
        if self.date_to:
            domain.append(('date', '<=', self.date_to))
        moves = StockMove.search(domain)
        series = {}
        wh_by_loc = {
            loc.id: wh
            for wh in (self.warehouse_ids or self.env['stock.warehouse'].search([]))
            for loc in wh.view_location_id.child_internal_loc_ids
        }
        for mv in moves:
            warehouse = None
            for wh_id, wh in wh_by_loc.items():
                if (mv.location_id.parent_path or '').startswith(
                        wh.view_location_id.parent_path):
                    warehouse = wh_id
                    break
            key = (mv.product_id.id, warehouse or 0)
            day = fields.Date.to_date(mv.date)
            series.setdefault(key, {})
            series[key][day] = series[key].get(day, 0.0) + mv.product_uom.qty
        return series

    @staticmethod
    def _feature_row(history, idx, date):
        """Numeric features from a daily history list ending at idx."""
        row = []
        window = history[max(0, idx - 28):idx + 1]
        lags = [history[idx - k] if idx - k >= 0 else 0.0 for k in (1, 7, 14)]
        row.extend(lags)
        r7 = sum(window[-7:]) / min(len(window), 7) or 0.0
        r28 = sum(window[-28:]) / len(window) if window else 0.0
        row.extend([r7, r28])
        row.extend([date.weekday(), date.month])
        return row

    # ------------------------------------------------------------- training
    def _build_dataset(self, series):
        X, y, keys, dates = [], [], [], []
        for (product_id, warehouse_id), by_day in series.items():
            days = sorted(by_day)
            hist = [by_day.get(d, 0.0) for d in days]
            full_range = []
            if days:
                cur = days[0]
                while cur <= days[-1]:
                    full_range.append(cur)
                    cur += timedelta(days=1)
            values = {d: by_day.get(d, 0.0) for d in full_range}
            hist_full = [values[d] for d in full_range]
            for i in range(len(full_range)):
                X.append(self._feature_row(hist_full, i, full_range[i]))
                y.append(hist_full[i])
                keys.append((product_id, warehouse_id))
                dates.append(full_range[i])
        return X, y, keys, dates

    def _make_estimator(self):
        self.ensure_one()
        if self.algorithm == 'rf':
            return RandomForestRegressor(
                n_estimators=self.n_estimators or 100,
                max_depth=self.max_depth or None, n_jobs=2, random_state=42)
        if self.algorithm == 'lr':
            return LinearRegression()
        return GradientBoostingRegressor(
            n_estimators=self.n_estimators or 100,
            max_depth=self.max_depth or 3,
            learning_rate=self.learning_rate or 0.1,
            min_samples_split=self.min_samples_split or 10,
            random_state=42)

    def _run_training(self, start_time=None):
        self.ensure_one()
        import time
        t0 = time.time()

        series = self._fetch_series()
        if not series:
            raise UserError(_(
                'No historical demand found for this scope. '
                'Check products/warehouses/date range.'))

        X, y, keys, dates = self._build_dataset(series)
        if len(X) < 30:
            raise UserError(_(
                'Not enough samples (%s) to train. Need at least 30.') % len(X))

        split = int(len(X) * 0.8)
        est = self._make_estimator()
        est.fit(X[:split], y[:split])

        val_pred = est.predict(X[split:])
        val_true = y[split:]
        mae = float(mean_absolute_error(val_true, val_pred))
        rmse = float(np.sqrt(np.mean((np.array(val_true) - val_pred) ** 2)))
        mask = [t != 0 for t in val_true]
        mape = float(np.mean([
            abs((t - p) / t) * 100 for t, p in zip(val_true, val_pred) if t
        ])) if any(mask) else 0.0
        bias = float(sum(p - t for t, p in zip(val_true, val_pred))
                     / max(len(val_true), 1))

        duration = time.time() - t0
        self.write({
            'mae': mae, 'rmse': rmse, 'mape': mape, 'bias': bias,
            'training_samples': split,
            'validation_samples': len(val_true),
            'training_duration': duration,
            'last_trained': fields.Datetime.now(),
        })

        # persist trained estimator as attachment
        payload = base64_encode(pickle.dumps(est))
        attach = self.model_attachment_id
        vals = {
            'name': f'{self.name}-model.pkl',
            'datas': payload,
            'res_model': self._name,
            'res_id': self.id,
        }
        if attach:
            attach.write(vals)
        else:
            self.model_attachment_id = \
                self.env['ir.attachment'].create(vals).id

        self.env['forecast.training.log'].create({
            'model_id': self.id,
            'status': 'success',
            'message': (f'Trained on {split} samples, '
                        f'validated on {len(val_true)}. '
                        f'MAE={mae:.2f} RMSE={rmse:.2f} MAPE={mape:.1f}%'),
        })
        self._generate_predictions(keys, dates, est)

    # ---------------------------------------------------------- predictions
    def _generate_predictions(self, keys=None, dates=None, est=None):
        self.ensure_one()
        cfg = self.env['forecast.config'].search([], limit=1)
        horizon = (cfg.prediction_horizon_days or 30) if cfg else 30
        confidence = (cfg.confidence_level or 0.95) if cfg else 0.95
        z = {0.90: 1.64, 0.95: 1.96, 0.99: 2.58}.get(round(confidence, 2), 1.96)

        if est is None:
            att = self.model_attachment_id
            if not att:
                raise UserError(_('Model not trained yet.'))
            est = pickle.loads(base64.b64decode(att.with_context(
                bin_size=False).datas))

        series = self._fetch_series()
        self.prediction_ids.unlink()
        today = fields.Date.today()
        created = 0
        for (product_id, warehouse_id), by_day in series.items():
            days = sorted(by_day)
            if not days:
                continue
            cur = days[0]
            full_range = []
            while cur <= max(days[-1], today):
                full_range.append(cur)
                cur += timedelta(days=1)
            hist = {d: by_day.get(d, 0.0) for d in full_range}
            buffer = [hist.get(d, 0.0) for d in full_range]
            sigma = max(np.std(buffer[-56:] or [0.0]), 0.5)
            future = today + timedelta(days=1)
            for step in range(horizon):
                d = future + timedelta(days=step)
                xrow = self._feature_row(buffer, len(buffer) - 1, d)
                pred = float(est.predict([xrow])[0])
                pred = max(pred, 0.0)
                delta = z * sigma
                self.env['forecast.prediction'].create({
                    'model_id': self.id,
                    'product_id': product_id,
                    'warehouse_id': warehouse_id or False,
                    'date': d,
                    'predicted_qty': round(pred, 2),
                    'lower_bound': round(max(pred - delta, 0.0), 2),
                    'upper_bound': round(pred + delta, 2),
                    'confidence': confidence,
                })
                created += 1
                buffer.append(pred)
        _logger.info('Forecast %s: %s predictions generated',
                     self.name, created)


def base64_encode(data: bytes) -> bytes:
    """Local helper to avoid importing odoo.tools here."""
    import base64 as _b
    return _b.b64encode(data)


class ForecastPrediction(models.Model):
    _name = 'forecast.prediction'
    _description = 'Demand Forecast Prediction'
    _order = 'date, product_id, warehouse_id'

    model_id = fields.Many2one('forecast.model', string='Model',
                               required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse')
    date = fields.Date(string='Date', required=True)
    predicted_qty = fields.Float(string='Predicted Quantity')
    lower_bound = fields.Float(string='Lower Bound (95%)')
    upper_bound = fields.Float(string='Upper Bound (95%)')
    confidence = fields.Float(string='Confidence Score', default=0.95)

    _sql_constraints = [
        ('unique_prediction',
         'unique(model_id, product_id, warehouse_id, date)',
         'Prediction already exists for this combination.'),
    ]


class ForecastConfig(models.Model):
    _name = 'forecast.config'
    _description = 'Forecast Global Configuration'

    name = fields.Char(default='Global Config')
    auto_retrain = fields.Boolean(string='Auto Retrain Models', default=True)
    retrain_frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], string='Retrain Frequency', default='weekly')
    prediction_horizon_days = fields.Integer(
        string='Prediction Horizon (days)', default=30)
    min_training_samples = fields.Integer(
        string='Min Training Samples', default=100)
    confidence_level = fields.Float(string='Confidence Level', default=0.95)
    service_level_target = fields.Float(string='Service Level Target',
                                        default=0.95)
