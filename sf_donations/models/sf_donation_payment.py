# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDonationPayment(models.Model):
    _name = 'sf.donation.payment'
    _description = 'Donation Payment'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    promise_id = fields.Many2one(
        'sf.donation.promise', string='Promise', ondelete='restrict',
        index=True)
    donor = fields.Char(string='Donor')
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 ondelete='set null')
    amount = fields.Float(string='Amount', required=True)
    payment_date = fields.Date(
        string='Payment date', default=fields.Date.context_today)
    method = fields.Selection([
        ('cash', 'Cash'),
        ('bank', 'Bank transfer'),
        ('online', 'Online'),
        ('other', 'Other'),
    ], string='Method', default='cash', required=True)
    campaign_id = fields.Many2one(
        'sf.donation.campaign', related='promise_id.campaign_id',
        store=True, readonly=True, index=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('received', 'Received'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.donation.payment')
        if not vals.get('donor') and vals.get('promise_id'):
            vals['donor'] = self.env['sf.donation.promise'].browse(
                vals['promise_id']).donor
        payment = super().create(vals)
        if payment.state == 'received':
            payment.promise_id._update_state_from_payments()
        return payment

    def action_receive(self):
        if not self.env.user.has_group('sf_donations.group_sf_donation_manager'):
            raise UserError(_('Only a donation manager can mark payments '
                              'as received.'))
        for payment in self:
            if payment.state != 'draft':
                raise UserError(_('Only draft payments can be received.'))
        self.state = 'received'
        self.mapped('promise_id')._update_state_from_payments()