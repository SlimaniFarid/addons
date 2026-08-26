# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDonationCampaign(models.Model):
    _name = 'sf.donation.campaign'
    _description = 'Donation Campaign'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    title = fields.Char(string='Title', required=True, tracking=True)
    target_amount = fields.Float(string='Target amount', tracking=True)
    start_date = fields.Date(string='Start date')
    end_date = fields.Date(string='End date')
    collected_amount = fields.Float(
        string='Collected amount', compute='_compute_collected_amount',
        store=True)
    promise_ids = fields.One2many(
        'sf.donation.promise', 'campaign_id', string='Promises')
    payment_ids = fields.One2many(
        'sf.donation.payment', 'campaign_id',
        compute='_compute_payment_ids', string='Payments', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('promise_ids.payment_ids')
    def _compute_payment_ids(self):
        for campaign in self:
            campaign.payment_ids = campaign.promise_ids.payment_ids

    @api.depends('payment_ids.state', 'payment_ids.amount')
    def _compute_collected_amount(self):
        for campaign in self:
            campaign.collected_amount = sum(
                campaign.payment_ids.filtered(
                    lambda p: p.state == 'received').mapped('amount'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.donation.campaign')
        return super().create(vals)

    def action_activate(self):
        for campaign in self:
            if campaign.state != 'draft':
                raise UserError(_('Only draft campaigns can be activated.'))
        self.state = 'active'

    def action_close(self):
        for campaign in self:
            if campaign.state != 'active':
                raise UserError(_('Only active campaigns can be closed.'))
        self.state = 'closed'