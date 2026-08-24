# -*- coding: utf-8 -*-
"""Tooling Request & Preparation models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfToolingRequest(models.Model):
    _name = 'sf.tooling.request'
    _description = 'Tooling Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    production_id = fields.Many2one('mrp.production', string='Production Order', required=True)
    tools_needed = fields.Text(string='Tools / Fixtures Needed', required=True)
    needed_for_date = fields.Date(string='Needed For')
    readiness = fields.Selection([
        ('pending', 'Pending'),
        ('ready', 'Ready'),
        ('missing', 'Missing Items'),
        ], string='Readiness', default=pending)
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('delayed', 'Delayed'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.tooling.request') or 'NEW'
        return super().create(vals_list)

    def action_preparing(self):
        self.write({'state': 'preparing'})

    def action_ready(self):
        self.write({'state': 'ready'})

    def action_delayed(self):
        self.write({'state': 'delayed'})

