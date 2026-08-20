# -*- coding: utf-8 -*-
import calendar
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


def _add_months(date, months):
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, calendar.monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)


class SfGymSubscription(models.Model):
    _name = 'sf.gym.subscription'
    _description = 'Gym Subscription'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    member_id = fields.Many2one(
        'sf.gym.member', string='Member', ondelete='restrict',
        index=True, tracking=True, required=True)
    plan_id = fields.Many2one(
        'sf.gym.plan', string='Plan', ondelete='restrict',
        index=True, tracking=True, required=True)
    start_date = fields.Date(
        string='Start date', default=fields.Date.context_today,
        required=True, tracking=True)
    end_date = fields.Date(
        string='End date', compute='_compute_end_date', store=True)
    price = fields.Float(
        string='Price', compute='_compute_price', store=True)
    paid = fields.Boolean(string='Paid', default=False, tracking=True)
    payment_ids = fields.One2many(
        'sf.gym.payment', 'subscription_id', string='Payments')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('start_date', 'plan_id.duration_months')
    def _compute_end_date(self):
        for subscription in self:
            if subscription.start_date and \
                    subscription.plan_id.duration_months:
                subscription.end_date = _add_months(
                    subscription.start_date,
                    subscription.plan_id.duration_months)
            else:
                subscription.end_date = False

    @api.depends('plan_id.price_monthly', 'plan_id.duration_months')
    def _compute_price(self):
        for subscription in self:
            subscription.price = subscription.plan_id.price_monthly * \
                subscription.plan_id.duration_months

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.gym.subscription')
        return super().create(vals)

    def action_activate(self):
        for subscription in self:
            if subscription.state != 'draft':
                raise UserError(_('Only draft subscriptions can be '
                                  'activated.'))
        self.state = 'active'

    def action_cancel(self):
        for subscription in self:
            if subscription.state not in ('draft', 'active'):
                raise UserError(_('Only draft or active subscriptions can '
                                  'be cancelled.'))
        self.state = 'cancelled'

    def _cron_expire_subscriptions(self):
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            self.with_company(company).search([
                ('state', '=', 'active'),
                ('end_date', '<', today),
            ]).write({'state': 'expired'})

    def _cron_gym_alerts(self):
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            subscriptions = self.with_company(company).search([
                ('state', '=', 'active'),
                ('paid', '=', False),
                ('end_date', '<=', today + timedelta(
                    days=company.sf_gym_alert_days)),
            ])
            for subscription in subscriptions:
                if subscription.activity_ids.filtered(
                        lambda a: a.activity_type_id == self.env.ref(
                            'mail.mail_activity_data_todo')):
                    continue
                subscription.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Subscription renewal alert: %s') %
                    subscription.name,
                    user_id=self.env.user.id)
            sessions = self.env['sf.gym.session'].with_company(
                company).search([
                    ('state', '=', 'confirmed'),
                    ('date', '=', today - timedelta(days=1)),
                    ('attendance_count', '=', 0),
                ])
            for session in sessions:
                if session.activity_ids.filtered(
                        lambda a: a.activity_type_id == self.env.ref(
                            'mail.mail_activity_data_todo')):
                    continue
                session.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Empty session alert: %s') % session.name,
                    user_id=self.env.user.id)
