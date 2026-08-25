# -*- coding: utf-8 -*-
"""Tax Deadline Calendar models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfTaxDeadline(models.Model):
    _name = 'sf.tax.deadline'
    _description = 'Tax Deadline'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    obligation = fields.Selection([
        ('vat', 'VAT Return'),
        ('corporate', 'Corporate Tax'),
        ('payroll', 'Payroll Taxes'),
        ('other', 'Other'),
        ], string='Obligation', required=True)
    due_date = fields.Date(string='Due Date', required=True)
    period_label = fields.Char(string='Period')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    amount_estimate = fields.Monetary(string='Estimated Amount')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('open', 'Open'),
        ('prepared', 'Prepared'),
        ('filed', 'Filed'),
        ('paid', 'Paid'),
        ], string='Status', default='open', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.tax.deadline') or 'NEW'
        return super().create(vals_list)

    def action_prepared(self):
        self.write({'state': 'prepared'})

    def action_filed(self):
        self.write({'state': 'filed'})

    def action_paid(self):
        self.write({'state': 'paid'})

