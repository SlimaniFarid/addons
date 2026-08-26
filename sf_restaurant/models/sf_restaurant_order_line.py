# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfRestaurantOrderLine(models.Model):
    _name = 'sf.restaurant.order.line'
    _description = 'Restaurant Order Line'
    _order = 'id'

    order_id = fields.Many2one('sf.restaurant.order', string='Order', required=True, ondelete='cascade')
    item_id = fields.Many2one('sf.restaurant.menu.item', string='Menu Item', required=True, ondelete='restrict')
    product_id = fields.Many2one('product.product', string='Product', ondelete='set null')
    description = fields.Char(string='Description')
    qty = fields.Float(string='Quantity', required=True, default=1.0)
    price_unit = fields.Monetary(string='Unit Price', currency_field='currency_id')
    subtotal = fields.Monetary(
        string='Subtotal',
        compute='_compute_subtotal',
        store=True,
        currency_field='currency_id',
    )
    notes = fields.Char(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('qty', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.qty * (line.price_unit or 0.0)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('price_unit') and vals.get('item_id'):
                item = self.env['sf.restaurant.menu.item'].browse(vals['item_id'])
                vals['price_unit'] = item.price_unit
        return super().create(vals_list)