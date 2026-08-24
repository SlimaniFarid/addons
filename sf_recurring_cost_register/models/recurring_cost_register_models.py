# -*- coding: utf-8 -*-
"""Recurring Cost Register models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfRecurring_cost_register(models.Model):
    _name = 'sf.recurring_cost_register'
    _description = 'Recurring Cost Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    label = fields.Char(string='Cost Label', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    monthly_amount = fields.Monetary(string='Monthly Amount', required=True)
    frequency = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('annual', 'Annual'),
        ], string='Frequency', default=monthly)
    renewal_date = fields.Date(string='Renewal Date')
    cost_center = fields.Char(string='Cost Center')
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
                    'sf.recurring_cost_register') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

