# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfDonationPromise(models.Model):
    _name = 'sf.donation.promise'
    _description = 'Donation Promise'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    campaign_id = fields.Many2one(
        'sf.donation.campaign', string='Campaign', ondelete='restrict',
        index=True, tracking=True)
    donor = fields.Char(string='Donor', tracking=True)
    partner_id = fields.Many2one('res.partner', string='Partner',
                                 ondelete='set null')
    amount = fields.Float(string='Amount', required=True, tracking=True)
    pledge_date = fields.Date(
        string='Pledge date', default=fields.Date.context_today,
        tracking=True)
    frequency = fields.Selection([
        ('once', 'One-time'),
        ('monthly', 'Monthly'),
    ], string='Frequency', default='once', required=True, tracking=True)
    payment_ids = fields.One2many(
        'sf.donation.payment', 'promise_id', string='Payments')
    paid_amount = fields.Float(
        string='Paid amount', compute='_compute_paid_amount', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('payment_ids.state', 'payment_ids.amount')
    def _compute_paid_amount(self):
        for promise in self:
            promise.paid_amount = sum(
                promise.payment_ids.filtered(
                    lambda p: p.state == 'received').mapped('amount'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.donation.promise')
        return super().create(vals)

    def action_confirm(self):
        for promise in self:
            if promise.state != 'draft':
                raise UserError(_('Only draft promises can be confirmed.'))
        self.state = 'pending'

    def action_cancel(self):
        for promise in self:
            if promise.state not in ('draft', 'pending'):
                raise UserError(_('Only draft or pending promises can be '
                                  'cancelled.'))
        self.state = 'cancelled'

    def _update_state_from_payments(self):
        for promise in self:
            if promise.state == 'cancelled':
                continue
            promise.state = 'paid' if promise.paid_amount >= promise.amount \
                else 'pending'

    def _cron_donation_reminders(self):
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            promises = self.with_company(company).search([
                ('state', 'in', ['pending']),
                ('payment_ids.state', 'not in', ['received']),
                ('pledge_date', '<=', today - timedelta(
                    days=company.sf_donation_reminder_days)),
            ])
            for promise in promises:
                if promise.activity_ids.filtered(
                        lambda a: a.activity_type_id == self.env.ref(
                            'mail.mail_activity_data_todo')):
                    continue
                promise.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Donation pledge reminder: %s') % promise.name,
                    user_id=self.env.user.id)