# -*- coding: utf-8 -*-
"""Data & Document Retention Schedule models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRetentionRule(models.Model):
    _name = 'sf.retention.rule'
    _description = 'Retention Rule'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    doc_type = fields.Char(string='Document Type', required=True)
    legal_basis = fields.Char(string='Legal Basis')
    retention_years = fields.Integer(string='Retention (years)', default=10, required=True)
    disposal_method = fields.Selection([
        ('delete', 'Secure Delete'),
        ('shred', 'Physical Shred'),
        ('archive', 'Archive'),
        ], string='Disposal', default=delete)
    last_review = fields.Date(string='Last Review')
    owner_id = fields.Many2one('res.users', string='Owner')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('review', 'Under Review'),
        ('archived', 'Archived'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.retention.rule') or 'NEW'
        return super().create(vals_list)

    def action_review(self):
        self.write({'state': 'review'})

    def action_archived(self):
        self.write({'state': 'archived'})

