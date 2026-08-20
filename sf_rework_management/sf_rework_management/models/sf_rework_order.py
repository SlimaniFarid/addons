# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfReworkOrder(models.Model):
    _name = 'sf.rework.order'
    _description = 'Rework Order'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.rework.management.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True, ondelete='restrict')
    lot_id = fields.Many2one('stock.lot', string='Lot', ondelete='restrict')
    qty = fields.Float(string='Quantity', required=True)
    assignee_id = fields.Many2one('res.users', string='Assignee')
    source = fields.Selection([
        ('production', 'Production'),
        ('quality', 'Quality'),
        ('customer_return', 'Customer Return'),
        ('other', 'Other'),
    ], string='Source', required=True, default='production')
    reason = fields.Char(string='Reason', required=True)
    description = fields.Text(string='Description')
    disposition = fields.Selection([
        ('rework', 'Rework'),
        ('scrap', 'Scrap'),
        ('use_as_is', 'Use As Is'),
        ('return_to_supplier', 'Return to Supplier'),
        ('other', 'Other'),
    ], string='Disposition', default='rework')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    actual_start_datetime = fields.Datetime(string='Start Time')
    actual_end_datetime = fields.Datetime(string='End Time')
    hourly_rate = fields.Monetary(string='Hourly Rate', required=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  related='company_id.currency_id', store=True, readonly=True)
    operation_ids = fields.One2many('sf.rework.operation', 'order_id',
                                    string='Operations')
    scrap_ids = fields.One2many('sf.rework.scrap', 'order_id',
                                string='Scrap')
    total_hours = fields.Float(string='Total Hours',
                               compute='_compute_costs', store=True)
    rework_cost = fields.Monetary(string='Rework Cost',
                                  compute='_compute_costs', store=True, currency_field='currency_id')
    scrap_value = fields.Monetary(string='Scrap Value',
                                  compute='_compute_costs', store=True, currency_field='currency_id')
    total_cost = fields.Monetary(string='Total Cost',
                                 compute='_compute_costs', store=True, currency_field='currency_id')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_qty_positive', 'CHECK (qty > 0)',
         'The rework quantity must be greater than zero.'),
        ('check_hourly_rate_positive', 'CHECK (hourly_rate >= 0)',
         'The hourly rate cannot be negative.'),
    ]

    @api.constrains('qty')
    def _check_qty(self):
        for order in self:
            if order.qty <= 0:
                raise ValidationError(_('The rework quantity must be greater than zero.'))

    @api.depends('operation_ids.hours', 'operation_ids.hourly_rate', 'scrap_ids.value')
    def _compute_costs(self):
        for order in self:
            order.total_hours = sum(order.operation_ids.mapped('hours'))
            order.rework_cost = sum(op.hours * op.hourly_rate for op in order.operation_ids)
            order.scrap_value = sum(order.scrap_ids.mapped('value'))
            order.total_cost = order.rework_cost + order.scrap_value

    @api.model
    def _default_hourly_rate(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_rework_management.default_hourly_rate')
        try:
            return float(param) if param else 0.0
        except (TypeError, ValueError):
            return 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.rework.order')
            if 'hourly_rate' not in vals:
                vals['hourly_rate'] = self._default_hourly_rate()
        return super().create(vals_list)

    def write(self, vals):
        if not self.env.context.get('allow_write_on_locked'):
            locked_states = ('completed', 'closed', 'cancelled')
            for order in self:
                if order.state in locked_states:
                    if not self.env.user.has_group('sf_rework_management.group_sf_rework_management_manager'):
                        raise UserError(_('A completed, closed or cancelled rework order cannot be modified.'))
        return super().write(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_rework_management.group_sf_rework_management_manager'):
            raise UserError(_('Only a rework manager can perform this action.'))

    def action_start(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft rework orders can be started.'))
        self.write({
            'state': 'in_progress',
            'actual_start_datetime': fields.Datetime.now(),
        })

    def action_complete(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress rework orders can be completed.'))
        self.write({
            'state': 'completed',
            'actual_end_datetime': fields.Datetime.now(),
        })

    def action_close(self):
        self.ensure_one()
        self._check_manager()
        if self.state != 'completed':
            raise UserError(_('Only completed rework orders can be closed.'))
        self.with_context(allow_write_on_locked=True).write({'state': 'closed'})

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state in ('completed', 'closed', 'cancelled'):
            raise UserError(_('A completed, closed or cancelled rework order cannot be cancelled.'))
        self.with_context(allow_write_on_locked=True).write({
            'state': 'cancelled',
            'actual_end_datetime': fields.Datetime.now(),
        })

    def _cron_escalation(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_rework_management.alert_days')
        alert_days = int(param) if param else 7
        domain = [('state', 'in', ('draft', 'in_progress'))]
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            cutoff = fields.Datetime.now() - timedelta(days=alert_days)
            orders = scoped.search(domain + [('actual_start_datetime', '<', cutoff)])
            for order in orders:
                order._sf_check_todo(
                    todo_type,
                    'Rework order %s still open' % order.name,
                    'This rework order has been in progress for more than %s days.'
                    % alert_days,
                )