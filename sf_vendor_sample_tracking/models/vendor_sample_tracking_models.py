# -*- coding: utf-8 -*-
"""Vendor Sample Request Tracking models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVendorSample(models.Model):
    _name = 'sf.vendor.sample'
    _description = 'Vendor Sample Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    product_desc = fields.Char(string='Sample Description', required=True)
    requested_date = fields.Date(string='Requested', default=fields.Date.today)
    received_date = fields.Date(string='Received')
    evaluation = fields.Text(string='Evaluation')
    approved_for_use = fields.Boolean(string='Approved for Use')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('received', 'Received'),
        ('evaluated', 'Evaluated'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.vendor.sample') or 'NEW'
        return super().create(vals_list)

    def action_received(self):
        self.write({'state': 'received'})

    def action_evaluated(self):
        self.write({'state': 'evaluated'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

