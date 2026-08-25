# -*- coding: utf-8 -*-
"""Quality Audit Program models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfQuality_audit_program(models.Model):
    _name = 'sf.quality_audit_program'
    _description = 'Quality Audit Program'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    audit_title = fields.Char(string='Audit Title', required=True)
    audit_type = fields.Selection([
        ('internal', 'Internal'),
        ('supplier', 'Supplier'),
        ('customer', 'Customer'),
        ], string='Type', required=True)
    planned_date = fields.Date(string='Planned Date', required=True)
    auditor_id = fields.Many2one('res.users', string='Lead Auditor')
    findings_count = fields.Integer(string='Findings')
    capa_ref = fields.Char(string='CAPA Reference')
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
                    'sf.quality_audit_program') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

