# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfEvent(models.Model):
    _name = 'sf.event'
    _description = 'Event'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.events.activity.mixin']
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    event_type = fields.Selection([
        ('conference', 'Conference'),
        ('seminar', 'Seminar'),
        ('workshop', 'Workshop'),
        ('trade_show', 'Trade Show'),
        ('other', 'Other'),
    ], string='Event Type', required=True, default='conference')
    start_date = fields.Date(string='Start Date', required=True)
    end_date = fields.Date(string='End Date', required=True)
    location = fields.Char(string='Location')
    capacity = fields.Integer(string='Capacity')
    budget = fields.Monetary(string='Budget', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    session_ids = fields.One2many('sf.event.session', 'event_id', string='Sessions')
    registration_ids = fields.One2many('sf.event.registration', 'event_id', string='Registrations')
    expense_ids = fields.One2many('sf.event.expense', 'event_id', string='Expenses')
    revenue = fields.Monetary(string='Revenue', compute='_compute_financials', store=True, currency_field='currency_id')
    expenses_total = fields.Monetary(string='Expenses Total', compute='_compute_financials', store=True, currency_field='currency_id')
    balance = fields.Monetary(string='Balance', compute='_compute_financials', store=True, currency_field='currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('registration_ids.price_unit', 'registration_ids.state', 'expense_ids.amount')
    def _compute_financials(self):
        for event in self:
            paid_states = ('confirmed', 'checked_in', 'done')
            event.revenue = sum(
                event.registration_ids.filtered(lambda r: r.state in paid_states).mapped('price_unit')
            )
            event.expenses_total = sum(event.expense_ids.mapped('amount'))
            event.balance = event.revenue - event.expenses_total

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.event')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_events.group_sf_events_manager'):
            raise UserError(_('Only an event manager can perform this action.'))

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft events can be confirmed.'))
        self.state = 'confirmed'

    def action_start(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed events can be started.'))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state not in ('confirmed', 'in_progress'):
            raise UserError(_('Only confirmed or in-progress events can be marked as done.'))
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state == 'done':
            raise UserError(_('A completed event cannot be cancelled.'))
        self.state = 'cancelled'

    def _cron_daily_alerts(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        companies = self.env['res.company'].search([])
        for company in companies:
            scoped = self.with_company(company)
            today = fields.Date.context_today(scoped)
            reminder_days = int(scoped.env['ir.config_parameter'].sudo().get_param(
                'sf_events.reminder_days', '7'
            ))
            upcoming = scoped.env['sf.event'].search([
                ('state', 'in', ('draft', 'confirmed')),
                ('start_date', '<=', today + timedelta(days=reminder_days)),
                ('start_date', '>=', today),
            ])
            for event in upcoming:
                event._sf_check_todo(
                    todo_type,
                    'Event %s starts within 7 days' % event.name,
                    'Reminder: the event starts on %s.' % event.start_date,
                )
            negative = scoped.env['sf.event'].search([
                ('state', 'in', ('confirmed', 'in_progress')),
            ]).filtered(lambda e: e.balance < 0)
            for event in negative:
                event._sf_check_todo(
                    todo_type,
                    'Event %s has a negative balance' % event.name,
                    'Reminder: the budget balance is negative (%s).' % event.balance,
                )