# -*- coding: utf-8 -*-
"""Customer Revenue Trend Alerts models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRevenueTrend(models.Model):
    _name = 'sf.revenue.trend'
    _description = 'Revenue Trend Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    period_current = fields.Date(string='Current Period', required=True)
    revenue_current = fields.Monetary(string='Current Revenue')
    revenue_previous = fields.Monetary(string='Previous Revenue')
    drop_percent = fields.Float(string='Drop %')
    action_taken = fields.Text(string='Action Taken')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('detected', 'Detected'),
        ('contacted', 'Contacted'),
        ('recovered', 'Recovered'),
        ('lost', 'Lost'),
        ], string='Status', default='detected', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.revenue.trend') or 'NEW'
        return super().create(vals_list)

    def action_contacted(self):
        self.write({'state': 'contacted'})

    def action_recovered(self):
        self.write({'state': 'recovered'})

    def action_lost(self):
        self.write({'state': 'lost'})

