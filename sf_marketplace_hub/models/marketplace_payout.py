# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MarketplacePayout(models.Model):
    _name = 'sf.marketplace.payout'
    _description = 'Marketplace Payout'
    _rec_name = 'name'
    _order = 'date desc, id desc'

    name = fields.Char(string='Number', required=True, readonly=True,
                       default=lambda self: _('New'))
    date = fields.Date(string='Date', required=True,
                       default=fields.Date.context_today)
    vendor_id = fields.Many2one(
        'sf.marketplace.vendor', string='Vendor', required=True,
        ondelete='cascade')
    marketplace_id = fields.Many2one(
        'sf.marketplace', string='Marketplace', required=True,
        ondelete='cascade')
    amount = fields.Monetary(
        string='Amount', compute='_compute_amount', store=True)
    currency_id = fields.Many2one(
        related='marketplace_id.currency_id', string='Currency',
        readonly=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    note = fields.Text(string='Note')

    @api.depends('vendor_id', 'vendor_id.commission_total',
                 'vendor_id.listing_ids.sold_amount')
    def _compute_amount(self):
        for payout in self:
            payout.amount = payout.vendor_id.commission_total or 0.0

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq = self.env['ir.sequence'].next_by_code('sf.marketplace.payout')
            vals['name'] = seq or '/'
        return super().create(vals)

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_pay(self):
        self.write({'state': 'paid'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})