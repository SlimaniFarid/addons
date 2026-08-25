# -*- coding: utf-8 -*-
"""Document Approval Reminders models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDocApprovalChase(models.Model):
    _name = 'sf.doc.approval.chase'
    _description = 'Approval Chase'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    document_ref = fields.Char(string='Document', required=True)
    pending_with_id = fields.Many2one('res.users', string='Pending With', required=True)
    sent_since = fields.Date(string='Sent Since', required=True)
    days_pending = fields.Integer(string='Days Pending')
    escalated = fields.Boolean(string='Escalated')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('reminded', 'Reminded'),
        ('escalated', 'Escalated'),
        ('approved', 'Approved'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.doc.approval.chase') or 'NEW'
        return super().create(vals_list)

    def action_reminded(self):
        self.write({'state': 'reminded'})

    def action_escalated(self):
        self.write({'state': 'escalated'})

    def action_approved(self):
        self.write({'state': 'approved'})

