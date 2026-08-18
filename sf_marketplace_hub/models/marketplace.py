# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Marketplace(models.Model):
    _name = 'sf.marketplace'
    _description = 'Marketplace'
    _rec_name = 'name'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, size=10)
    sequence = fields.Integer(string='Sequence', default=10)
    active = fields.Boolean(string='Active', default=True)
    description = fields.Text(string='Description')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company)
    currency_id = fields.Many2one(
        'res.currency', string='Currency', required=True,
        default=lambda self: self.env.company.currency_id)
    vendor_ids = fields.One2many(
        'sf.marketplace.vendor', 'marketplace_id', string='Vendors')
    listing_ids = fields.One2many(
        'sf.marketplace.listing', 'marketplace_id', string='Listings')
    payout_ids = fields.One2many(
        'sf.marketplace.payout', 'marketplace_id', string='Payouts')
    vendor_count = fields.Integer(
        string='Vendor Count', compute='_compute_counts')
    listing_count = fields.Integer(
        string='Listing Count', compute='_compute_counts')
    gmv_total = fields.Monetary(
        string='GMV Total', compute='_compute_totals',
        currency_field='currency_id')
    commission_total = fields.Monetary(
        string='Commission Total', compute='_compute_totals',
        currency_field='currency_id')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Marketplace code must be unique.'),
    ]

    @api.depends('vendor_ids', 'listing_ids')
    def _compute_counts(self):
        for mkt in self:
            mkt.vendor_count = len(mkt.vendor_ids)
            mkt.listing_count = len(mkt.listing_ids)

    @api.depends('listing_ids', 'listing_ids.commission_amount')
    def _compute_totals(self):
        for mkt in self:
            mkt.gmv_total = sum(
                mkt.listing_ids.mapped('sold_amount') or [0.0])
            mkt.commission_total = sum(
                mkt.listing_ids.mapped('commission_amount') or [0.0])