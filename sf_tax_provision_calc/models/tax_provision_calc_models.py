# -*- coding: utf-8 -*-
"""Tax Provision Calculator models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfTax_provision_calc(models.Model):
    _name = 'sf.tax_provision_calc'
    _description = 'Tax Provision Calculator'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    fiscal_year = fields.Integer(string='Fiscal Year', required=True)
    pretax_income = fields.Monetary(string='Pre-Tax Income')
    tax_rate_percent = fields.Float(string='Tax Rate %', default=25.0)
    current_tax = fields.Monetary(string='Current Tax')
    deferred_tax = fields.Monetary(string='Deferred Tax')
    notes = fields.Text(string='Notes')
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
                    'sf.tax_provision_calc') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

