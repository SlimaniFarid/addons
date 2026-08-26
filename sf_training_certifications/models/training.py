# -*- coding: utf-8 -*-
from odoo import fields, models


class Training(models.Model):
    _name = 'sf.training'
    _description = 'Training'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    category_id = fields.Many2one('sf.training.category',
                                  string='Category', required=True)
    duration_hours = fields.Float(string='Duration (hours)', default=1.0)
    mandatory = fields.Boolean(string='Mandatory')
    active = fields.Boolean(string='Active', default=True)
    description = fields.Text(string='Description')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)