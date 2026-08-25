# -*- coding: utf-8 -*-
"""Quality Alert Aging Monitor models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQalertAging(models.Model):
    _name = 'sf.qalert.aging'
    _description = 'Alert Aging Entry'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    alert_ref = fields.Char(string='Alert Ref', required=True)
    opened_date = fields.Date(string='Opened', required=True)
    owner_id = fields.Many2one('res.users', string='Owner')
    aging_days = fields.Integer(string='Aging (days)')
    escalation_level = fields.Selection([
        ('none', 'None'),
        ('manager', 'Manager'),
        ('director', 'Director'),
        ], string='Escalation', default=none)
    blocker = fields.Text(string='Blocker')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('escalated', 'Escalated'),
        ('closed', 'Closed'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.qalert.aging') or 'NEW'
        return super().create(vals_list)

    def action_escalated(self):
        self.write({'state': 'escalated'})

    def action_closed(self):
        self.write({'state': 'closed'})

