# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfGymPayment(models.Model):
    _name = 'sf.gym.payment'
    _description = 'Gym Payment'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    subscription_id = fields.Many2one(
        'sf.gym.subscription', string='Subscription', ondelete='restrict',
        index=True, tracking=True, required=True)
    partner_id = fields.Many2one(
        'res.partner', string='Partner', ondelete='set null', index=True)
    amount = fields.Float(string='Amount', required=True, tracking=True)
    payment_date = fields.Date(
        string='Payment date', default=fields.Date.context_today,
        tracking=True)
    method = fields.Selection([
        ('cash', 'Cash'),
        ('transfer', 'Transfer'),
        ('card', 'Card'),
    ], string='Method', default='cash', required=True, tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.gym.payment')
        if not vals.get('partner_id') and vals.get('subscription_id'):
            subscription = self.env['sf.gym.subscription'].browse(
                vals['subscription_id'])
            if subscription.member_id.partner_id:
                vals['partner_id'] = subscription.member_id.partner_id.id
        payment = super().create(vals)
        if payment.state == 'done':
            payment.subscription_id.paid = True
        return payment

    def action_done(self):
        if not (self.env.user.has_group(
                'sf_gym_fitness.group_sf_gym_manager') or
                self.env.user.has_group(
                'sf_gym_fitness.group_sf_gym_user')):
            raise UserError(_('Only a gym user or manager can record '
                              'payments.'))
        for payment in self:
            if payment.state != 'draft':
                raise UserError(_('Only draft payments can be marked as '
                                  'done.'))
        self.state = 'done'
        self.mapped('subscription_id').paid = True
