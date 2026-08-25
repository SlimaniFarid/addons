# -*- coding: utf-8 -*-
"""Blanket Order Release Tracking models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfBlanketOrder(models.Model):
    _name = 'sf.blanket.order'
    _description = 'Blanket Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Vendor', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    total_quantity = fields.Float(string='Total Quantity')
    released_quantity = fields.Float(string='Released')
    unit_price = fields.Float(string='Unit Price')
    expiry_date = fields.Date(string='Expiry Date')
    remaining = fields.Float(string='Remaining')
    currency_id = fields.Many2one(related='company_id.currency_id')
    state = fields.Selection([
        ('active', 'Active'),
        ('exhausted', 'Exhausted'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ], string='Status', default='active', tracking=True, copy=False)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.blanket.order') or 'NEW'
        return super().create(vals_list)

    def action_exhausted(self):
        self.write({'state': 'exhausted'})

    def action_expired(self):
        self.write({'state': 'expired'})

    def action_cancelled(self):
        self.write({'state': 'cancelled'})

