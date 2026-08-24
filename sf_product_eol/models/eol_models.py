# -*- coding: utf-8 -*-
"""Product end-of-life records."""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfProductEol(models.Model):
    _name = 'sf.product.eol'
    _description = 'Product End-of-Life'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'eol_date asc'

    name = fields.Char(string='Reference', required=True, copy=False,
                       readonly=True, default='New')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True, tracking=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    announcement_date = fields.Date(string='Announcement Date',
                                    default=fields.Date.today)
    eol_date = fields.Date(string='EOL Date', required=True)
    last_time_buy_date = fields.Date(string='Last-Time-Buy Date')
    replacement_product_id = fields.Many2one('product.product',
                                             string='Replacement Product')
    remaining_stock = fields.Float(string='Remaining Stock',
                                   compute='_compute_open_data')
    open_sale_orders = fields.Integer(string='Open Sale Orders',
                                      compute='_compute_open_data')
    open_order_lines = fields.Integer(string='Open Order Lines',
                                      compute='_compute_open_data')
    communication_plan = fields.Html(string='Customer Communication Plan')
    state = fields.Selection([
        ('announced', 'Announced'), ('phaseout', 'Phase-Out'),
        ('discontinued', 'Discontinued'), ('cancelled', 'Cancelled')],
        default='announced', tracking=True)
    discontinued_on = fields.Date(string='Discontinued On', readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.product.eol') or 'EOL-NEW'
        return super().create(vals_list)

    def _compute_open_data(self):
        for rec in self:
            quants = sum(self.env['stock.quant'].search([
                ('product_id', '=', rec.product_id.id),
                ('location_id.usage', '=', 'internal')]).mapped('quantity'))
            rec.remaining_stock = quants
            orders = self.env['sale.order.line'].search([
                ('product_id', '=', rec.product_id.id),
                ('order_id.state', 'in', ('sale', 'done'))])
            rec.open_sale_orders = len(orders.mapped('order_id'))
            rec.open_order_lines = len(orders)

    def action_phaseout(self):
        self.write({'state': 'phaseout'})

    def action_discontinue(self):
        self.ensure_one()
        if self.open_sale_orders:
            raise UserError(_(
                '%s open sale orders remain on this product. Convert or '
                'cancel them before discontinuing.')
                % self.open_sale_orders)
        self.product_id.write({'sale_ok': False})
        self.write({'state': 'discontinued',
                    'discontinued_on': fields.Date.today()})

    def action_cancel(self):
        self.write({'state': 'cancelled'})
