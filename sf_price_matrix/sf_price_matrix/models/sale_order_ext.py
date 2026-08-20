# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SaleOrderExt(models.Model):
    _inherit = 'sale.order'

    price_matrix_category_id = fields.Many2one(
        'sf.price.matrix.category', string='Price Matrix Category')

    @api.onchange('partner_id')
    def _onchange_partner_category(self):
        if self.partner_id and self.partner_id.price_matrix_category_id:
            self.price_matrix_category_id = (
                self.partner_id.price_matrix_category_id)

    def _compute_price_matrix_discounts(self):
        """Apply matrix discounts to order lines."""
        for order in self:
            if not order.price_matrix_category_id:
                continue
            Rule = self.env['sf.price.matrix.rule']
            for line in order.order_line:
                if not line.product_id:
                    continue
                discount = Rule.compute_discount(
                    order.price_matrix_category_id, line.product_id,
                    line.product_uom_qty)
                line.discount = discount or 0.0