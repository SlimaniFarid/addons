# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfRestaurantOrder(models.Model):
    _name = 'sf.restaurant.order'
    _description = 'Restaurant Order'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.restaurant.activity.mixin']
    _order = 'order_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    table_id = fields.Many2one('sf.restaurant.table', string='Table', required=True, ondelete='restrict')
    service = fields.Selection([
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ], string='Service', required=True)
    line_ids = fields.One2many('sf.restaurant.order.line', 'order_id', string='Lines')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('transmitted', 'Transmitted'),
        ('prepared', 'Prepared'),
        ('served', 'Served'),
        ('closed', 'Closed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    total = fields.Monetary(
        string='Total',
        compute='_compute_total',
        store=True,
        currency_field='currency_id',
    )
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    order_date = fields.Date(string='Order Date', default=fields.Date.context_today)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('line_ids.subtotal')
    def _compute_total(self):
        for order in self:
            order.total = sum(order.line_ids.mapped('subtotal'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.restaurant.order')
            if not vals.get('table_id'):
                raise UserError(_('An order requires a table.'))
            active = self.env['sf.restaurant.order'].search([
                ('table_id', '=', vals['table_id']),
                ('state', 'in', ('draft', 'transmitted', 'prepared', 'served')),
            ])
            if active:
                raise UserError(_('This table already has an active order.'))
        orders = super().create(vals_list)
        for order in orders:
            order.table_id.write({'state': 'occupied', 'current_order_id': order.id})
        return orders

    def _check_manager(self):
        if not self.env.user.has_group('sf_restaurant.group_sf_restaurant_manager'):
            raise UserError(_('Only a restaurant manager can perform this action.'))

    def _check_item_availability(self, line_vals):
        self.ensure_one()
        item = self.env['sf.restaurant.menu.item'].browse(line_vals.get('item_id'))
        service_map = {
            'breakfast': item.available_breakfast,
            'lunch': item.available_lunch,
            'dinner': item.available_dinner,
        }
        if not service_map.get(self.service):
            raise UserError(_('This menu item is not available for the %s service.') % self.service)

    def write(self, vals):
        if 'line_ids' in vals:
            for order in self:
                for command in vals['line_ids']:
                    if isinstance(command, (list, tuple)) and len(command) > 1 and command[0] == 0:
                        order._check_item_availability(command[1])
        if vals.get('state') == 'closed':
            self._check_manager()
        return super().write(vals)

    def action_transmit(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft orders can be transmitted to the kitchen.'))
        if not self.line_ids:
            raise UserError(_('The order has no lines to transmit.'))
        self.state = 'transmitted'
        return self.env.ref('sf_restaurant.report_kitchen_ticket').report_action(self)

    def action_prepare(self):
        self.ensure_one()
        if self.state != 'transmitted':
            raise UserError(_('Only transmitted orders can be prepared.'))
        self.state = 'prepared'

    def action_serve(self):
        self.ensure_one()
        if self.state != 'prepared':
            raise UserError(_('Only prepared orders can be served.'))
        self.state = 'served'

    def action_close(self):
        self.ensure_one()
        if self.state != 'served':
            raise UserError(_('Only served orders can be closed.'))
        self.state = 'closed'
        self.table_id.write({'state': 'cleaning', 'current_order_id': False})
        return self.env.ref('sf_restaurant.report_table_bill').report_action(self)

    def action_force_close(self):
        self.ensure_one()
        if self.state in ('closed', 'cancelled'):
            raise UserError(_('A %s order cannot be force closed.') % self.state)
        self._check_manager()
        self.state = 'closed'
        self.table_id.write({'state': 'cleaning', 'current_order_id': False})

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'closed':
            raise UserError(_('A closed order cannot be cancelled.'))
        if self.state != 'draft':
            self._check_manager()
        self.state = 'cancelled'
        if self.table_id.current_order_id == self:
            self.table_id.write({'current_order_id': False, 'state': 'free'})