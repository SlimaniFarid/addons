# -*- coding: utf-8 -*-
"""Business Glossary & Data Dictionary models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfGlossaryTerm(models.Model):
    _name = 'sf.glossary.term'
    _description = 'Glossary Term'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    term = fields.Char(string='Term', required=True)
    definition = fields.Html(string='Definition')
    source_system = fields.Char(string='Source System')
    owner_id = fields.Many2one('res.users', string='Term Owner')
    related_kpis = fields.Char(string='Related KPIs')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('deprecated', 'Deprecated'),
        ], string='Status', default=draft)
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('deprecated', 'Deprecated'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.glossary.term') or 'NEW'
        return super().create(vals_list)

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_deprecated(self):
        self.write({'state': 'deprecated'})

