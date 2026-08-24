# -*- coding: utf-8 -*-
"""Churn Prediction Rules Engine models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfChurn_prediction_rules(models.Model):
    _name = 'sf.churn_prediction_rules'
    _description = 'Churn Prediction Rules Engine'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    rule_name = fields.Char(string='Rule Name', required=True)
    signal_type = fields.Selection([
        ('usage_decline', 'Usage Decline'),
        ('support_tickets', 'Support Tickets Up'),
        ('champion_left', 'Champion Left'),
        ('no_orders', 'No Recent Orders'),
        ], string='Signal', required=True)
    weight = fields.Float(string='Weight', default=1.0)
    threshold = fields.Float(string='Alert Threshold')
    alert_action = fields.Text(string='Alert Action')
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
                    'sf.churn_prediction_rules') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

