# -*- coding: utf-8 -*-
from odoo import fields, models, _


class PriceMatrixCategory(models.Model):
    _name = 'sf.price.matrix.category'
    _description = 'Customer Category'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    description = fields.Text(string='Description')
    default_discount = fields.Float(string='Default Discount %', default=0.0)
    rule_ids = fields.One2many('sf.price.matrix.rule', 'category_id',
                               string='Price Rules')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Category code must be unique.'),
    ]