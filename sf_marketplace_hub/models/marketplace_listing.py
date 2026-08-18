# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MarketplaceListing(models.Model):
    _name = 'sf.marketplace.listing'
    _description = 'Marketplace Listing'
    _rec_name = 'product_id'
    _order = 'product_id'

    product_id = fields.Many2one(
        'product.product', string='Product', required=True,
        ondelete='cascade')
    vendor_id = fields.Many2one(
        'sf.marketplace.vendor', string='Vendor', required=True,
        ondelete='cascade')
    marketplace_id = fields.Many2one(
        'sf.marketplace', string='Marketplace', required=True,
        ondelete='cascade')
    active = fields.Boolean(string='Active', default=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('listed', 'Listed'),
        ('paused', 'Paused'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    list_price = fields.Monetary(
        string='List Price', related='product_id.list_price')
    sold_qty = fields.Float(string='Sold Qty', default=0.0)
    sold_amount = fields.Monetary(
        string='Sold Amount', compute='_compute_sold', store=True)
    commission_amount = fields.Monetary(
        string='Commission', compute='_compute_sold', store=True)
    currency_id = fields.Many2one(
        related='marketplace_id.currency_id', string='Currency',
        readonly=True)

    @api.depends('sold_qty', 'list_price', 'vendor_id.commission_rate')
    def _compute_sold(self):
        for listing in self:
            rate = listing.vendor_id.commission_rate or 0.0
            sold = listing.sold_qty * (listing.list_price or 0.0)
            listing.sold_amount = sold
            listing.commission_amount = sold * rate / 100.0

    def action_list(self):
        self.write({'state': 'listed'})

    def action_pause(self):
        self.write({'state': 'paused'})

    def action_close(self):
        self.write({'state': 'closed'})