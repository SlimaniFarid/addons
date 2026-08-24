# -*- coding: utf-8 -*-
"""Incident On-Call Escalation models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfIncident_oncall(models.Model):
    _name = 'sf.incident_oncall'
    _description = 'Incident On-Call Escalation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    incident_type = fields.Char(string='Incident Type', required=True)
    l1_user_id = fields.Many2one('res.users', string='L1 Responder', required=True)
    l2_user_id = fields.Many2one('res.users', string='L2 Escalation')
    l3_user_id = fields.Many2one('res.users', string='L3 Escalation')
    escalation_minutes = fields.Integer(string='Escalate After (min)', default=15)
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
                    'sf.incident_oncall') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

