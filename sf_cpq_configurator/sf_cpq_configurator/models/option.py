# -*- coding: utf-8 -*-
from odoo import fields, models, _


class CpqOption(models.Model):
    _name = 'sf.cpq.option'
    _description = 'CPQ Option'
    _rec_name = 'name'
    _order = 'sequence, name'

    attribute_id = fields.Many2one('sf.cpq.attribute', string='Attribute',
                                   required=True, ondelete='cascade')
    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    price_adjust = fields.Float(string='Price Adjustment', default=0.0,
                                help="Added to or deducted from the base "
                                     "product price.")
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(attribute_id, code)',
         'Option code must be unique per attribute.'),
    ]