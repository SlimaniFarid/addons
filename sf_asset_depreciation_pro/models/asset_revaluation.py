# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class AssetRevaluation(models.Model):
    _name = 'sf.asset.depreciation.pro.asset.revaluation'
    _description = 'Asset Revaluation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    currency_id = fields.Many2one(related='company_id.currency_id', store=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, store=True, default=lambda self: self.env.company)

    asset_id = fields.Many2one(comodel_name='account.asset', ondelete='restrict')
    old_value = fields.Monetary(string='Old Value', currency_field='currency_id')
    new_value = fields.Monetary(string='New Value', currency_field='currency_id')
    reason = fields.Text(string='Reason', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)

