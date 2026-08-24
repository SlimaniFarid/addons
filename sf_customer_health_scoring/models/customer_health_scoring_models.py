# -*- coding: utf-8 -*-
"""Customer Health Scoring Rules models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_health_scoring(models.Model):
    _name = 'sf.customer_health_scoring'
    _description = 'Customer Health Scoring Rules'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rule_name = fields.Char(string='Rule Name', required=True)
    signal = fields.Selection([
        ('login_drop', 'Login Drop'),
        ('support_escalation', 'Support Escalation'),
        ('payment_late', 'Payment Late'),
        ('usage_decline', 'Usage Decline'),
        ], string='Signal', required=True)
    weight = fields.Float(string='Weight', default=1.0)
    threshold = fields.Float(string='Alert Threshold')
    active = fields.Boolean(string='Active', default=True)
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
                    'sf.customer_health_scoring') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

