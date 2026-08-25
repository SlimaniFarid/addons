# -*- coding: utf-8 -*-
"""Prepaid Expense Amortization models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfPrepaid(models.Model):
    _name = 'sf.prepaid'
    _description = 'Prepaid Expense'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    label = fields.Char(string='Label', required=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    total_amount = fields.Monetary(string='Total Prepaid', required=True)
    start_date = fields.Date(string='Start Date', required=True)
    months = fields.Integer(string='Months', default=12)
    monthly_amort = fields.Float(string='Monthly Amortization')
    remaining = fields.Float(string='Remaining')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('fully_amortized', 'Fully Amortized'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.prepaid') or 'NEW'
        return super().create(vals_list)

    def action_fully_amortized(self):
        self.write({'state': 'fully_amortized'})

