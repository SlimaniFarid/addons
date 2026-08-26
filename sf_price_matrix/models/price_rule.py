# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class PriceMatrixRule(models.Model):
    _name = 'sf.price.matrix.rule'
    _description = 'Price Matrix Rule'
    _rec_name = 'product_id'
    _order = 'category_id, product_id'

    category_id = fields.Many2one('sf.price.matrix.category',
                                  string='Category', required=True,
                                  ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product',
                                 required=True)
    tier_ids = fields.Many2many('sf.price.matrix.tier',
                                string='Discount Tiers')
    max_discount = fields.Float(string='Max Discount %', default=50.0,
                                help="Safety limit for this product.")
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('product_uniq', 'unique(category_id, product_id)',
         'Only one rule per category and product.'),
    ]

    @api.model
    def compute_discount(self, category, product, quantity):
        """Return the discount % for a category/product/quantity."""
        rule = self.search([
            ('category_id', '=', category.id),
            ('product_id', '=', product.id),
            ('active', '=', True),
        ], limit=1)
        if not rule:
            return category.default_discount or 0.0
        tiers = rule.tier_ids.filtered(lambda t: quantity >= t.min_qty)
        if tiers:
            best = max(tiers, key=lambda t: t.discount)
            return min(best.discount, rule.max_discount)
        return min(category.default_discount or 0.0, rule.max_discount)