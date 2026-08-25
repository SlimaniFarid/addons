# -*- coding: utf-8 -*-
"""User Activity Summary models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfUser_activity_log(models.Model):
    _name = 'sf.user_activity_log'
    _description = 'User Activity Summary'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    log_date = fields.Date(string='Date', required=True, default=fields.Date.today)
    user_id = fields.Many2one('res.users', string='User', required=True)
    login_count = fields.Integer(string='Logins')
    records_created = fields.Integer(string='Records Created')
    records_modified = fields.Integer(string='Records Modified')
    anomaly_note = fields.Text(string='Anomaly Notes')
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
                    'sf.user_activity_log') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

