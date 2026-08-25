# -*- coding: utf-8 -*-
"""Competitive Intelligence Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfCompetitive_intel_register(models.Model):
    _name = 'sf.competitive_intel_register'
    _description = 'Competitive Intelligence Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    competitor = fields.Char(string='Competitor', required=True)
    intel_type = fields.Selection([
        ('product', 'Product Update'),
        ('pricing', 'Pricing Change'),
        ('partnership', 'Partnership'),
        ('leadership', 'Leadership Change'),
        ], string='Type', required=True)
    details = fields.Html(string='Details')
    impact = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ], string='Impact', default=medium)
    source = fields.Char(string='Source')
    date = fields.Date(string='Date', default=fields.Date.today)
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
                    'sf.competitive_intel_register') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

