# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MarketplaceVendor(models.Model):
    _name = 'sf.marketplace.vendor'
    _description = 'Marketplace Vendor'
    _rec_name = 'partner_id'
    _order = 'partner_id'

    partner_id = fields.Many2one(
        'res.partner', string='Vendor', required=True, ondelete='cascade')
    marketplace_id = fields.Many2one(
        'sf.marketplace', string='Marketplace', required=True,
        ondelete='cascade')
    active = fields.Boolean(string='Active', default=True)
    commission_rate = fields.Float(
        string='Commission Rate (%)', default=10.0,
        help="Percentage of sales kept as marketplace commission.")
    payout_account_id = fields.Many2one(
        'account.journal', string='Payout Account',
        help="Bank account used for vendor payouts.")
    listing_ids = fields.One2many(
        'sf.marketplace.listing', 'vendor_id', string='Listings')
    payout_ids = fields.One2many(
        'sf.marketplace.payout', 'vendor_id', string='Payouts')
    sales_total = fields.Monetary(
        string='Sales Total', compute='_compute_totals')
    commission_total = fields.Monetary(
        string='Commission Total', compute='_compute_totals')
    listing_count = fields.Integer(
        string='Listing Count', compute='_compute_totals')
    currency_id = fields.Many2one(
        related='marketplace_id.currency_id', string='Currency',
        readonly=True)

    _sql_constraints = [
        ('partner_marketplace_uniq', 'unique(partner_id, marketplace_id)',
         'A vendor can only appear once per marketplace.'),
    ]

    @api.depends('listing_ids', 'listing_ids.sold_amount',
                 'listing_ids.commission_amount')
    def _compute_totals(self):
        for vendor in self:
            vendor.sales_total = sum(
                vendor.listing_ids.mapped('sold_amount') or [0.0])
            vendor.commission_total = sum(
                vendor.listing_ids.mapped('commission_amount') or [0.0])
            vendor.listing_count = len(vendor.listing_ids)

    def name_get(self):
        result = []
        for vendor in self:
            name = vendor.partner_id.name or ''
            if vendor.marketplace_id:
                name = '%s (%s)' % (name, vendor.marketplace_id.name)
            result.append((vendor.id, name))
        return result