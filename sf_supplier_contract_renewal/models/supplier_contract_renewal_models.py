# -*- coding: utf-8 -*-
"""Supplier Contract Renewal Tracker models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_contract_renewal(models.Model):
    _name = 'sf.supplier_contract_renewal'
    _description = 'Supplier Contract Renewal Tracker'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    contract_ref = fields.Char(string='Contract Ref', required=True)
    expiry_date = fields.Date(string='Expiry Date', required=True)
    annual_value = fields.Monetary(string='Annual Value')
    performance_ok = fields.Boolean(string='Performance Satisfactory')
    renegotiation_note = fields.Text(string='Renegotiation Notes')
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
                    'sf.supplier_contract_renewal') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

