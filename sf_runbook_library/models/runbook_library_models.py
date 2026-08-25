# -*- coding: utf-8 -*-
"""Runbook & Procedure Library models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRunbook(models.Model):
    _name = 'sf.runbook'
    _description = 'Runbook'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Title', required=True)
    system = fields.Char(string='System / Process')
    content = fields.Html(string='Procedure Steps')
    version = fields.Char(string='Version', default=1.0)
    owner_id = fields.Many2one('res.users', string='Owner')
    last_review = fields.Date(string='Last Review')
    next_review = fields.Date(string='Next Review')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('review_due', 'Review Due'),
        ('archived', 'Archived'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.runbook') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_review_due(self):
        self.write({'state': 'review_due'})

    def action_archived(self):
        self.write({'state': 'archived'})

