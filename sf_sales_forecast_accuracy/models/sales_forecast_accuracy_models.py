# -*- coding: utf-8 -*-
"""Sales Forecast Accuracy Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSales_forecast_accuracy(models.Model):
    _name = 'sf.sales_forecast_accuracy'
    _description = 'Sales Forecast Accuracy Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    period = fields.Char(string='Period', required=True)
    rep_id = fields.Many2one('res.users', string='Sales Rep')
    forecast_amount = fields.Monetary(string='Forecast')
    actual_amount = fields.Monetary(string='Actual')
    accuracy_percent = fields.Float(string='Accuracy %')
    bias = fields.Selection([
        ('over', 'Over-forecast'),
        ('under', 'Under-forecast'),
        ('accurate', 'Accurate'),
        ], string='Bias')
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
                    'sf.sales_forecast_accuracy') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

