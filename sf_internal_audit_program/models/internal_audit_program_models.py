# -*- coding: utf-8 -*-
"""Internal Audit Annual Program models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfInternalAudit(models.Model):
    _name = 'sf.internal.audit'
    _description = 'Internal Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    audit_title = fields.Char(string='Audit Title', required=True)
    scope = fields.Html(string='Scope')
    planned_date = fields.Date(string='Planned Date')
    lead_auditor_id = fields.Many2one('res.users', string='Lead Auditor')
    findings_count = fields.Integer(string='Findings')
    report_ref = fields.Char(string='Report Reference')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('reported', 'Reported'),
        ('closed', 'Closed'),
        ], string='Status', default='planned', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.internal.audit') or 'NEW'
        return super().create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_reported(self):
        self.write({'state': 'reported'})

    def action_closed(self):
        self.write({'state': 'closed'})

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.internal.audit'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
