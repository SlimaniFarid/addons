# -*- coding: utf-8 -*-
"""Budget vs Actual Alerts models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBudgetAlert(models.Model):
    _name = 'sf.budget.alert'
    _description = 'Budget Alert'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    department = fields.Char(string='Department', required=True)
    period_month = fields.Date(string='Period', required=True)
    budget_amount = fields.Monetary(string='Budget', required=True)
    actual_amount = fields.Monetary(string='Actual', required=True)
    consumption_percent = fields.Float(string='Consumed %')
    alert_level = fields.Selection([
        ('ok', 'OK'),
        ('warn', 'Warning 80%'),
        ('exceeded', 'Exceeded'),
        ], string='Alert')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('explained', 'Explained'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.budget.alert') or 'NEW'
        return super().create(vals_list)

    def action_explained(self):
        self.write({'state': 'explained'})

    def action_closed(self):
        self.write({'state': 'closed'})

