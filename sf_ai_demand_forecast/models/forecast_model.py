import json
import logging
import hashlib
from datetime import timedelta
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


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
    product_ids = fields.Many2many('product.product', string='Products',
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
    use_promos = fields.Boolean(string='Use Promo Features', default=True)
    use_price = fields.Boolean(string='Use Price Features', default=False)

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
    validation_samples = fields.Integer(string='Validation Samples', readonly=True)
    training_duration = fields.Float(string='Training Duration (s)', readonly=True)
    last_trained = fields.Datetime(string='Last Trained', readonly=True)
    error_message = fields.Text(string='Error', readonly=True)

    prediction_ids = fields.One2many('forecast.prediction', 'model_id', string='Predictions')
    training_log_ids = fields.One2many('forecast.training.log', 'model_id', string='Training Logs')

    def action_train(self):
        for model in self:
            model.state = 'training'
            model.error_message = False
            try:
                # Simplified training - in reality would use actual ML
                model._run_training()
                model.state = 'trained'
            except Exception as e:
                _logger.exception('Training failed')
                model.state = 'failed'
                model.error_message = str(e)

    def _run_training(self):
        """Simplified training logic"""
        self.ensure_one()
        import time
        start = time.time()
        # In real implementation: fetch data, feature engineering, train sklearn model
        # Save model pickle to attachment
        # Compute metrics on validation set
        self.write({
            'mae': 12.5,
            'mape': 8.3,
            'rmse': 18.2,
            'bias': -1.2,
            'training_samples': 10000,
            'validation_samples': 2000,
            'training_duration': time.time() - start,
            'last_trained': fields.Datetime.now(),
        })
        self.env['forecast.training.log'].create({
            'model_id': self.id,
            'status': 'success',
            'message': 'Training completed',
        })


class ForecastPrediction(models.Model):
    _name = 'forecast.prediction'
    _description = 'Demand Forecast Prediction'
    _order = 'date, product_id, warehouse_id'

    model_id = fields.Many2one('forecast.model', string='Model', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', required=True)
    date = fields.Date(string='Date', required=True)
    predicted_qty = fields.Float(string='Predicted Quantity')
    lower_bound = fields.Float(string='Lower Bound (95%)')
    upper_bound = fields.Float(string='Upper Bound (95%)')
    confidence = fields.Float(string='Confidence Score', default=0.95)

    _sql_constraints = [
        ('unique_prediction', 'unique(model_id, product_id, warehouse_id, date)',
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
    prediction_horizon_days = fields.Integer(string='Prediction Horizon (days)', default=30)
    min_training_samples = fields.Integer(string='Min Training Samples', default=100)
    confidence_level = fields.Float(string='Confidence Level', default=0.95)
    service_level_target = fields.Float(string='Service Level Target', default=0.95)


class ForecastTrainingLog(models.Model):
    _name = 'forecast.training.log'
    _description = 'Forecast Training Log'
    _order = 'create_date desc'

    model_id = fields.Many2one('forecast.model', string='Model', required=True, ondelete='cascade')
    status = fields.Selection([
        ('started', 'Started'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ], string='Status')
    message = fields.Text(string='Message')
    metrics = fields.Text(string='Metrics (JSON)')