# -*- coding: utf-8 -*-
from odoo import fields, models


class SfRestaurantMenuCategory(models.Model):
    _name = 'sf.restaurant.menu.category'
    _description = 'Restaurant Menu Category'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True, copy=False)
    sequence = fields.Integer(string='Sequence', default=10)
    product_ids = fields.One2many('sf.restaurant.menu.item', 'category_id', string='Menu Items')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.restaurant.menu.category')
        return super().create(vals_list)