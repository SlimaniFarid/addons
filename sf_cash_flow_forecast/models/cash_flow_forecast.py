# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CashFlowForecast(models.Model):
    _name = 'sf.cashflow.forecast'
    _description = 'Cash Flow Forecast'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(
        string='Forecast Name',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        copy=False,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.cashflow.forecast')
        return super().create(vals_list)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    date_from = fields.Date(
        string='Start Date',
        required=True,
        default=fields.Date.context_today,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    horizon_days = fields.Integer(
        string='Horizon (days)',
        default=30,
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='Number of days to project cash flow forward from the start date.',
    )
    date_to = fields.Date(
        string='End Date',
        compute='_compute_date_to',
        store=True,
    )
    bank_journal_ids = fields.Many2many(
        'account.journal',
        string='Bank / Cash Journals',
        readonly=True,
        states={'draft': [('readonly', False)]},
        domain="[('type', 'in', ['bank', 'cash'])]",
        help='Journals whose accounts are included in the cash position.',
    )
    opening_balance = fields.Monetary(
        string='Opening Balance',
        currency_field='currency_id',
        compute='_compute_balances',
        store=True,
    )
    total_inflow = fields.Monetary(
        string='Total Inflow',
        currency_field='currency_id',
        compute='_compute_balances',
        store=True,
    )
    total_outflow = fields.Monetary(
        string='Total Outflow',
        currency_field='currency_id',
        compute='_compute_balances',
        store=True,
    )
    net_cash_flow = fields.Monetary(
        string='Net Cash Flow',
        currency_field='currency_id',
        compute='_compute_balances',
        store=True,
    )
    closing_balance = fields.Monetary(
        string='Closing Balance',
        currency_field='currency_id',
        compute='_compute_balances',
        store=True,
    )
    minimum_balance = fields.Monetary(
        string='Minimum Balance',
        currency_field='currency_id',
        compute='_compute_balances',
        store=True,
    )
    minimum_date = fields.Date(
        string='Minimum Date',
        compute='_compute_balances',
        store=True,
    )
    alert_threshold = fields.Monetary(
        string='Alert Threshold',
        currency_field='currency_id',
        default=0.0,
        readonly=True,
        states={'draft': [('readonly', False)]},
        help='Warn when the projected balance falls below this value.',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        tracking=True,
    )
    line_ids = fields.One2many(
        'sf.cashflow.line',
        'forecast_id',
        string='Cash Flow Lines',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    inflow_line_ids = fields.One2many(
        'sf.cashflow.line',
        'forecast_id',
        string='Inflow Lines',
        domain=[('direction', '=', 'inflow')],
    )
    outflow_line_ids = fields.One2many(
        'sf.cashflow.line',
        'forecast_id',
        string='Outflow Lines',
        domain=[('direction', '=', 'outflow')],
    )
    alert_ids = fields.One2many(
        'sf.cashflow.alert',
        'forecast_id',
        string='Alerts',
    )

    @api.depends('date_from', 'horizon_days')
    def _compute_date_to(self):
        for forecast in self:
            forecast.date_to = forecast.date_from + timedelta(
                days=forecast.horizon_days)

    @api.depends(
        'date_from',
        'horizon_days',
        'bank_journal_ids',
        'line_ids.date',
        'line_ids.amount',
    )
    def _compute_balances(self):
        for forecast in self:
            opening = forecast._compute_opening_balance()
            inflow = 0.0
            outflow = 0.0
            running = opening
            minimum = opening
            minimum_date = forecast.date_from or False
            for line in forecast.line_ids.sorted('date'):
                if line.date and forecast.date_from and \
                        line.date < forecast.date_from:
                    continue
                if line.direction == 'inflow':
                    inflow += line.amount
                    running += line.amount
                else:
                    outflow += line.amount
                    running -= line.amount
                if running < minimum:
                    minimum = running
                    minimum_date = line.date
            forecast.opening_balance = opening
            forecast.total_inflow = inflow
            forecast.total_outflow = outflow
            forecast.net_cash_flow = inflow - outflow
            forecast.closing_balance = opening + inflow - outflow
            forecast.minimum_balance = minimum
            forecast.minimum_date = minimum_date

    def _compute_opening_balance(self):
        self.ensure_one()
        if not self.bank_journal_ids:
            return 0.0
        lines = self.env['account.move.line'].search([
            ('journal_id', 'in', self.bank_journal_ids.ids),
            ('move_id.state', '=', 'posted'),
            ('date', '<=', self.date_from),
        ])
        return sum(lines.mapped('amount_residual')) if lines else 0.0

    def action_generate_lines(self):
        """Recompute the projection from accounting data (receivables,
        payables and confirmed purchase orders)."""
        self.ensure_one()
        lines = self.env['sf.cashflow.line']
        for forecast in self:
            generated = forecast.line_ids.filtered(
                lambda line: line.source == 'auto')
            generated.unlink()

            recv_domain = [
                ('move_id.state', '=', 'posted'),
                ('account_id.account_type', 'in',
                 ['asset_receivable', 'liability_payable']),
                ('date_maturity', '!=', False),
                ('amount_residual', '!=', 0.0),
            ]
            move_lines = self.env['account.move.line'].search(recv_domain)
            for line in move_lines:
                if line.account_id.account_type == 'asset_receivable':
                    direction = 'inflow'
                    if line.amount_residual < 0:
                        continue
                    amount = abs(line.amount_residual)
                else:
                    direction = 'outflow'
                    if line.amount_residual > 0:
                        continue
                    amount = abs(line.amount_residual)
                lines.create({
                    'forecast_id': forecast.id,
                    'date': line.date_maturity,
                    'direction': direction,
                    'source': 'auto',
                    'partner_id': line.partner_id.id or False,
                    'account_id': line.account_id.id,
                    'name': line.move_id.name or line.name,
                    'amount': amount,
                    'move_line_id': line.id,
                })

            porders = self.env['purchase.order'].search([
                ('state', 'in', ['draft', 'sent', 'confirmed']),
                ('date_planned', '!=', False),
            ])
            for order in porders:
                lines.create({
                    'forecast_id': forecast.id,
                    'date': order.date_planned,
                    'direction': 'outflow',
                    'source': 'auto',
                    'partner_id': order.partner_id.id or False,
                    'name': order.name,
                    'amount': order.amount_total,
                    'purchase_order_id': order.id,
                })
        return True

    def action_confirm(self):
        self.write({'state': 'confirmed'})
        for forecast in self:
            forecast._update_alerts()

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})

    def action_regenerate_alerts(self):
        self.ensure_one()
        self._update_alerts()
        return True

    def _update_alerts(self):
        self.ensure_one()
        self.alert_ids.unlink()
        if not self.alert_threshold:
            return
        running = self.opening_balance
        previous_date = self.date_from
        for line in self.line_ids.sorted('date'):
            if line.date and self.date_from and line.date < self.date_from:
                continue
            if line.date != previous_date and running < self.alert_threshold:
                self.env['sf.cashflow.alert'].create({
                    'forecast_id': self.id,
                    'date': previous_date,
                    'projected_balance': running,
                    'company_id': self.company_id.id,
                })
            if line.direction == 'inflow':
                running += line.amount
            else:
                running -= line.amount
            previous_date = line.date
        if running < self.alert_threshold:
            self.env['sf.cashflow.alert'].create({
                'forecast_id': self.id,
                'date': self.date_to,
                'projected_balance': running,
                'company_id': self.company_id.id,
            })


class CashFlowLine(models.Model):
    _name = 'sf.cashflow.line'
    _description = 'Cash Flow Line'
    _order = 'date asc, id asc'

    forecast_id = fields.Many2one(
        'sf.cashflow.forecast',
        string='Forecast',
        required=True,
        ondelete='cascade',
    )
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='forecast_id.company_id',
        store=True,
        readonly=True,
    )
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        related='forecast_id.currency_id',
        store=True,
        readonly=True,
    )
    date = fields.Date(
        string='Date',
        required=True,
    )
    direction = fields.Selection(
        [
            ('inflow', 'Inflow'),
            ('outflow', 'Outflow'),
        ],
        string='Direction',
        required=True,
    )
    source = fields.Selection(
        [
            ('auto', 'Automatic'),
            ('manual', 'Manual'),
        ],
        string='Source',
        required=True,
        default='manual',
    )
    partner_id = fields.Many2one('res.partner', string='Partner')
    account_id = fields.Many2one('account.account', string='Account')
    name = fields.Char(
        string='Description',
        required=True,
    )
    amount = fields.Monetary(
        string='Amount',
        currency_field='currency_id',
        required=True,
    )
    move_line_id = fields.Many2one(
        'account.move.line',
        string='Source Journal Item',
        ondelete='set null',
    )
    purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Source Purchase Order',
        ondelete='set null',
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
    )

    @api.constrains('amount')
    def _check_amount(self):
        for line in self:
            if line.amount < 0:
                raise ValidationError(
                    _('Cash flow line amount must be positive. '
                      'Use the direction to indicate inflow or outflow.')
                )


class CashFlowAlert(models.Model):
    _name = 'sf.cashflow.alert'
    _description = 'Cash Flow Alert'
    _order = 'date asc, id asc'

    forecast_id = fields.Many2one(
        'sf.cashflow.forecast',
        string='Forecast',
        required=True,
        ondelete='cascade',
    )
    company_id = fields.Many2one('res.company', string='Company')
    date = fields.Date(string='Date')
    projected_balance = fields.Monetary(
        string='Projected Balance',
        currency_field='currency_id',
    )
    currency_id = fields.Many2one(
        'res.currency',
        related='forecast_id.currency_id',
        store=True,
        readonly=True,
    )
    is_processed = fields.Boolean(
        string='Processed',
        default=False,
    )

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.cashflow.forecast'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    def action_confirm(self):
        res = super().action_confirm()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res


# --- wave_final ---
class _RefreshBusiness(models.Model):
    _inherit = 'sf.cashflow.forecast'

    def action_refresh_business(self):
        """Pull open / overdue amounts for linked partner."""
        for rec in self:
            partner = getattr(rec, 'partner_id', False)
            if not partner:
                continue
            moves = self.env['account.move'].search([
                ('move_type', '=', 'out_invoice'),
                ('state', '=', 'posted'),
                ('partner_id', '=', partner.id)])
            open_amt = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
            ).mapped('amount_residual'))
            today = fields.Date.context_today(rec)
            overdue = sum(moves.filtered(
                lambda m: m.payment_state in ('not_paid', 'partial')
                and m.invoice_date_due
                and m.invoice_date_due < today
            ).mapped('amount_residual'))
            rec.message_post(body=_(
                'Open: {o:.2f}, Overdue: {d:.2f} '
                '({c} posted invoice(s)).').format(
                o=open_amt, d=overdue, c=len(moves)))
        return True
