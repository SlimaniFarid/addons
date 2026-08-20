# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDonationReceipt(models.Model):
    _name = 'sf.donation.receipt'
    _description = 'Donation Receipt'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 ondelete='set null')
    donor = fields.Char(string='Donor')
    amount = fields.Float(string='Amount', required=True)
    receipt_date = fields.Date(
        string='Receipt date', default=fields.Date.context_today)
    fiscal_ref = fields.Char(string='Fiscal reference')
    payment_id = fields.Many2one(
        'sf.donation.payment', string='Payment', ondelete='set null',
        index=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('issued', 'Issued'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.donation.receipt')
        if vals.get('payment_id'):
            payment = self.env['sf.donation.payment'].browse(
                vals['payment_id'])
            if not vals.get('amount'):
                vals['amount'] = payment.amount
            if not vals.get('donor'):
                vals['donor'] = payment.donor
        return super().create(vals)

    def action_issue(self):
        if not self.env.user.has_group('sf_donations.group_sf_donation_manager'):
            raise UserError(_('Only a donation manager can issue receipts.'))
        for receipt in self:
            if receipt.state != 'draft':
                raise UserError(_('Only draft receipts can be issued.'))
        self.state = 'issued'