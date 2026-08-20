# -*- coding: utf-8 -*-
from odoo import fields, models, _


class DiscountTier(models.Model):
    _name = 'sf.price.matrix.tier'
    _description = 'Discount Tier'
    _rec_name = 'name'
    _order = 'sequence'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    min_qty = fields.Float(string='Minimum Quantity', required=True,
                           default=1.0)
    discount = fields.Float(string='Discount %', required=True, default=0.0)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('qty_uniq', 'unique(min_qty)', 'Tier minimum must be unique.'),
    ]