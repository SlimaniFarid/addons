# -*- coding: utf-8 -*-
"""Compliance Obligation Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCompliance_obligation(models.Model):
    _name = 'sf.compliance_obligation'
    _description = 'Compliance Obligation Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    obligation = fields.Char(string='Obligation', required=True)
    regulation = fields.Char(string='Regulation / Standard', required=True)
    requirement = fields.Text(string='Requirement', required=True)
    evidence_ref = fields.Char(string='Evidence Reference')
    deadline = fields.Date(string='Deadline')
    owner_id = fields.Many2one('res.users', string='Owner')
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
                    'sf.compliance_obligation') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

