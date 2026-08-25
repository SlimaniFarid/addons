# -*- coding: utf-8 -*-
"""3-Way Match Monitor models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_invoice_3way_match2(models.Model):
    _name = 'sf.supplier_invoice_3way_match2'
    _description = '3-Way Match Monitor'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    po_ref = fields.Char(string='PO Ref')
    receipt_ref = fields.Char(string='Receipt Ref')
    invoice_ref = fields.Char(string='Invoice Ref', required=True)
    match_status = fields.Selection([
        ('matched', 'Matched'),
        ('qty_mismatch', 'Qty Mismatch'),
        ('price_mismatch', 'Price Mismatch'),
        ], string='Match', required=True)
    exception_note = fields.Text(string='Exception')
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
                    'sf.supplier_invoice_3way_match2') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

