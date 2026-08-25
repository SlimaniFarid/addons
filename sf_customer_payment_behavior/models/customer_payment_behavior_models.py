# -*- coding: utf-8 -*-
"""Customer Payment Behavior Analysis models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_payment_behavior(models.Model):
    _name = 'sf.customer_payment_behavior'
    _description = 'Customer Payment Behavior Analysis'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    avg_days_to_pay = fields.Float(string='Avg Days to Pay')
    trend = fields.Selection([
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('worsening', 'Worsening'),
        ], string='Trend', default=stable)
    risk_score = fields.Integer(string='Risk Score (0-100)')
    credit_action = fields.Text(string='Recommended Credit Action')
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
                    'sf.customer_payment_behavior') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

