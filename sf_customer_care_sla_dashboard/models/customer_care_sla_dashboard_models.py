# -*- coding: utf-8 -*-
"""Care SLA Dashboard Config models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCustomer_care_sla_dashboard(models.Model):
    _name = 'sf.customer_care_sla_dashboard'
    _description = 'Care SLA Dashboard Config'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    metric_name = fields.Char(string='Metric', required=True)
    tier = fields.Selection([
        ('platinum', 'Platinum'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('bronze', 'Bronze'),
        ], string='Tier', required=True)
    target = fields.Float(string='Target')
    alert_threshold = fields.Float(string='Alert Threshold')
    breach_action = fields.Text(string='Breach Action')
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
                    'sf.customer_care_sla_dashboard') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

