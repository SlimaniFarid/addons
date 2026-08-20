# -*- coding: utf-8 -*-
from odoo import fields, models


class ItAssetCategory(models.Model):
    _name = 'sf.it.asset.category'
    _description = 'IT Asset Category'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    parent_id = fields.Many2one('sf.it.asset.category',
                                string='Parent Category')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company)