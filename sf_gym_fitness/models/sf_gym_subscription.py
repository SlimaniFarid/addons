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

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.gym.attendance'

    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
    is_overdue = fields.Boolean(
        string='Overdue', compute='_boost_is_overdue',
        store=True)

    @api.depends('end_date', 'state')
    def _boost_is_overdue(self):
        today = fields.Date.context_today(self)
        for rec in self:
            dl = rec.end_date
            terminal = False

            terminal = rec.state in ('done', 'cancelled', 'closed', 'resolved', 'expired', 'rejected', 'obsolete', 'archived')

            val = dl
            if val is not None and hasattr(val, 'hour'):
                val = val.date()
            elif val is not None and not hasattr(val, 'year'):
                try:
                    import datetime as _dt
                    val = _dt.date.fromisoformat(str(val)[:10])
                except ValueError:
                    val = None
            rec.is_overdue = bool(val) and not terminal and val < today

    def action_done(self):
        res = super().action_done()
        for rec in self:
                vals = {'Record': rec.display_name or rec.name}
                vals['Responsible'] = rec.user_id.name
                vals['Deadline'] = str(rec.end_date)
                rec.message_post(body=', '.join('%s: %s' % kv for kv in vals.items()))
        return res

