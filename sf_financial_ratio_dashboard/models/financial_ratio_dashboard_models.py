# -*- coding: utf-8 -*-
"""Financial Ratio Calculator models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfFinancial_ratio_dashboard(models.Model):
    _name = 'sf.financial_ratio_dashboard'
    _description = 'Financial Ratio Calculator'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period_label = fields.Char(string='Period', required=True)
    total_assets = fields.Monetary(string='Total Assets')
    total_liabilities = fields.Monetary(string='Total Liabilities')
    revenue = fields.Monetary(string='Revenue')
    net_income = fields.Monetary(string='Net Income')
    current_ratio = fields.Float(string='Current Ratio')
    debt_ratio = fields.Float(string='Debt Ratio')
    currency_id = fields.Many2one(related='company_id.currency_id')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.financial_ratio_dashboard') or 'NEW'
        return super().create(vals_list)


