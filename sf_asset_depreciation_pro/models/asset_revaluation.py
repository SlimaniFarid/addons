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

    asset_id = fields.account.asset(string='Asset Id')
    old_value = fields.Old(string='Old Value')
    new_value = fields.New(string='New Value')
    reason = fields.Reason(string='Reason', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)

