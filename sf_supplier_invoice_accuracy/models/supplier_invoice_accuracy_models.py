# -*- coding: utf-8 -*-
"""Supplier Invoice Accuracy Monitor models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_invoice_accuracy(models.Model):
    _name = 'sf.supplier_invoice_accuracy'
    _description = 'Supplier Invoice Accuracy Monitor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    period = fields.Char(string='Period', required=True)
    invoices_received = fields.Integer(string='Invoices Received')
    invoices_with_errors = fields.Integer(string='With Errors')
    error_rate_percent = fields.Float(string='Error Rate %')
    top_error_type = fields.Char(string='Top Error Type')
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
                    'sf.supplier_invoice_accuracy') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

