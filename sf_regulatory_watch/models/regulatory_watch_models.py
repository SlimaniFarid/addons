# -*- coding: utf-8 -*-
"""Regulatory Watch Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRegWatch(models.Model):
    _name = 'sf.reg.watch'
    _description = 'Regulation Watch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    regulation = fields.Char(string='Regulation', required=True)
    jurisdiction = fields.Char(string='Jurisdiction')
    effective_date = fields.Date(string='Effective Date')
    impact_level = fields.Selection([
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ], string='Impact', required=True, default=medium, tracking=True)
    impact_analysis = fields.Html(string='Impact Analysis')
    readiness_percent = fields.Float(string='Readiness %')
    owner_id = fields.Many2one('res.users', string='Owner')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('identified', 'Identified'),
        ('analyzed', 'Analyzed'),
        ('in_progress', 'In Progress'),
        ('compliant', 'Compliant'),
        ], string='Status', default='identified', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.reg.watch') or 'NEW'
        return super().create(vals_list)

    def action_analyzed(self):
        self.write({'state': 'analyzed'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_compliant(self):
        self.write({'state': 'compliant'})

