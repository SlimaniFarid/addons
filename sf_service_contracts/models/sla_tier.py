# -*- coding: utf-8 -*-
from odoo import fields, models, _


class SlaTier(models.Model):
    _name = 'sf.sla.tier'
    _description = 'SLA Tier'
    _rec_name = 'name'
    _order = 'sequence'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    response_hours = fields.Integer(string='Response Time (hours)',
                                    required=True, default=4)
    resolution_hours = fields.Integer(string='Resolution Time (hours)',
                                      required=True, default=24)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Tier code must be unique.'),
    ]