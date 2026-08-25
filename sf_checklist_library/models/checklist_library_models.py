# -*- coding: utf-8 -*-
"""Reusable Checklist Library models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfChecklistTemplate(models.Model):
    _name = 'sf.checklist.template'
    _description = 'Checklist Template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    title = fields.Char(string='Checklist Title', required=True)
    purpose = fields.Text(string='Purpose')
    items = fields.Text(string='Items (one per line)', required=True)
    owner_id = fields.Many2one('res.users', string='Owner')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
        ], string='Status', default='draft', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.checklist.template') or 'NEW'
        return super().create(vals_list)

    def action_active(self):
        self.write({'state': 'active'})

    def action_archived(self):
        self.write({'state': 'archived'})

