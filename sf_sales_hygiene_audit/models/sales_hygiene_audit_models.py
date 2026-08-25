# -*- coding: utf-8 -*-
"""Pipeline Hygiene Audit models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPipelineAudit(models.Model):
    _name = 'sf.pipeline.audit'
    _description = 'Pipeline Audit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    audit_date = fields.Date(string='Audit Date', required=True, default=fields.Date.today)
    stale_opportunities = fields.Integer(string='Stale Opportunities')
    missing_next_step = fields.Integer(string='Missing Next Step')
    overdue_close = fields.Integer(string='Overdue Close Dates')
    cleanup_campaign = fields.Html(string='Cleanup Campaign')
    auditor_id = fields.Many2one('res.users', string='Auditor')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('actions', 'Actions Assigned'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.pipeline.audit') or 'NEW'
        return super().create(vals_list)

    def action_done(self):
        self.write({'state': 'done'})

    def action_actions(self):
        self.write({'state': 'actions'})

