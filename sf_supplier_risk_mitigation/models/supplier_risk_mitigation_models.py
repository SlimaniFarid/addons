# -*- coding: utf-8 -*-
"""Supplier Risk Mitigation Plan models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_risk_mitigation(models.Model):
    _name = 'sf.supplier_risk_mitigation'
    _description = 'Supplier Risk Mitigation Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    risk_description = fields.Text(string='Risk Description', required=True)
    mitigation_type = fields.Selection([
        ('dual_sourcing', 'Dual Sourcing'),
        ('inventory_buffer', 'Inventory Buffer'),
        ('contract_clause', 'Contract Clause'),
        ('exit_plan', 'Exit Plan'),
        ], string='Mitigation', required=True)
    implementation_date = fields.Date(string='Implementation Date')
    status_note = fields.Text(string='Status')
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
                    'sf.supplier_risk_mitigation') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

