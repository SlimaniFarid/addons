# -*- coding: utf-8 -*-
"""API Integration Monitor models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfApi_integration_log(models.Model):
    _name = 'sf.api_integration_log'
    _description = 'API Integration Monitor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    integration_name = fields.Char(string='Integration', required=True)
    endpoint = fields.Char(string='Endpoint')
    direction = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ], string='Direction', required=True)
    status = fields.Selection([
        ('success', 'Success'),
        ('error', 'Error'),
        ('timeout', 'Timeout'),
        ], string='Status', required=True)
    latency_ms = fields.Float(string='Latency (ms)')
    error_message = fields.Text(string='Error')
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
                    'sf.api_integration_log') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

