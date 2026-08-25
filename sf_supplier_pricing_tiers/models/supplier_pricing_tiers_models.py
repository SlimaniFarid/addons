# -*- coding: utf-8 -*-
"""Supplier Pricing Tiers models"""
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfSupplier_pricing_tiers(models.Model):
    _name = 'sf.supplier_pricing_tiers'
    _description = 'Supplier Pricing Tiers'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda s: s.env.company, tracking=True)
    vendor_id = fields.Many2one('res.partner', string='Supplier', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    tier_1_qty = fields.Float(string='Tier 1 Qty')
    tier_1_price = fields.Float(string='Tier 1 Price')
    tier_2_qty = fields.Float(string='Tier 2 Qty')
    tier_2_price = fields.Float(string='Tier 2 Price')
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
                    'sf.supplier_pricing_tiers') or 'NEW'
        return super().create(vals_list)

    def action_submitted(self):
        self.write({'state': 'submitted'})

    def action_done(self):
        self.write({'state': 'done'})

