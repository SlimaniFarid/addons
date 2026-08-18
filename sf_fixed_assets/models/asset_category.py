# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AssetCategory(models.Model):
    _name = 'sf.fixed.asset.category'
    _description = 'Asset Category'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', size=10)
    useful_life_months = fields.Integer(
        string='Useful Life (months)', default=60,
        help="Default depreciation period in months.")
    depreciation_method = fields.Selection([
        ('straight_line', 'Straight Line'),
        ('declining', 'Declining Balance'),
    ], string='Depreciation Method', default='straight_line')
    account_id = fields.Many2one('account.account', string='Asset Account')
    active = fields.Boolean(string='Active', default=True)
    asset_ids = fields.One2many('sf.fixed.asset', 'category_id',
                                string='Assets')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Category name must be unique.'),
    ]