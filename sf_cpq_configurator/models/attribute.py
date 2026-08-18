# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class CpqAttribute(models.Model):
    _name = 'sf.cpq.attribute'
    _description = 'CPQ Attribute'
    _rec_name = 'name'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    description = fields.Text(string='Description')
    option_ids = fields.One2many('sf.cpq.option', 'attribute_id',
                                 string='Options')
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Attribute name must be unique.'),
    ]