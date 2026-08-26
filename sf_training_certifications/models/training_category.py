# -*- coding: utf-8 -*-
from odoo import fields, models


class TrainingCategory(models.Model):
    _name = 'sf.training.category'
    _description = 'Training Category'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')