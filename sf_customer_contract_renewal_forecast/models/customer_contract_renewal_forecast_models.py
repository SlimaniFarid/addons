# -*- coding: utf-8 -*-
"""Renewal Revenue Forecast models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_contract_renewal_forecast(models.Model):
    _name = 'sf.customer_contract_renewal_forecast'
    _description = 'Renewal Revenue Forecast'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    forecast_month = fields.Date(string='Forecast Month', required=True)
    contracts_expiring = fields.Integer(string='Contracts Expiring')
    revenue_at_risk = fields.Monetary(string='Revenue at Risk')
    historical_win_rate = fields.Float(string='Historical Win Rate %')
    forecast_revenue = fields.Monetary(string='Forecast Renewal Revenue')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('done', 'Done'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.customer_contract_renewal_forecast') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

