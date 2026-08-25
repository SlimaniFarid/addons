# -*- coding: utf-8 -*-
"""System Health Check models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSystem_health_check(models.Model):
    _name = 'sf.system_health_check'
    _description = 'System Health Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    check_date = fields.Date(string='Check Date', required=True, default=fields.Date.today)
    db_size_gb = fields.Float(string='DB Size (GB)')
    disk_free_percent = fields.Float(string='Disk Free %')
    active_users = fields.Integer(string='Active Users')
    avg_response_ms = fields.Float(string='Avg Response (ms)')
    alerts = fields.Text(string='Alerts')
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
                    'sf.system_health_check') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

