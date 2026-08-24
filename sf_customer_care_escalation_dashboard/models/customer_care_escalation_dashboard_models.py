# -*- coding: utf-8 -*-
"""Escalation Dashboard Config models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_escalation_dashboard(models.Model):
    _name = 'sf.customer_care_escalation_dashboard'
    _description = 'Escalation Dashboard Config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    metric = fields.Char(string='Metric', required=True)
    metric_type = fields.Selection([
        ('open_escalations', 'Open Escalations'),
        ('avg_resolution_time', 'Avg Resolution'),
        ('sla_breach_rate', 'SLA Breach Rate'),
        ], string='Type', required=True)
    target = fields.Float(string='Target')
    alert_threshold = fields.Float(string='Alert Threshold')
    team_routing = fields.Char(string='Team Routing')
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
                    'sf.customer_care_escalation_dashboard') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

