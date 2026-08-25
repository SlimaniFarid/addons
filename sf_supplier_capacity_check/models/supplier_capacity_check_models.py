# -*- coding: utf-8 -*-
"""Supplier Capacity Check models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplierCapacity(models.Model):
    _name = 'sf.supplier.capacity'
    _description = 'Capacity Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    requested_qty = fields.Float(string='Requested Qty')
    confirmed_capacity = fields.Float(string='Confirmed Capacity')
    lead_time_confirmed = fields.Integer(string='Confirmed Lead Time (days)')
    notes = fields.Text(string='Notes')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('requested', 'Requested'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ], string='Status', default='requested', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.supplier.capacity') or 'NEW'
        return super().create(vals_list)

    def action_confirmed(self):
        self.write({'state': 'confirmed'})

    def action_rejected(self):
        self.write({'state': 'rejected'})

