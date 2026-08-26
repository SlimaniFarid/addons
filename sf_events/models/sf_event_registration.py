# -*- coding: utf-8 -*-
from odoo import fields, models
from odoo.exceptions import UserError


class SfEventRegistration(models.Model):
    _name = 'sf.event.registration'
    _description = 'Event Registration'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.events.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    event_id = fields.Many2one('sf.event', string='Event', required=True, ondelete='cascade')
    session_ids = fields.Many2many('sf.event.session', string='Sessions')
    partner_id = fields.Many2one('res.partner', string='Customer', ondelete='set null')
    attendee_name = fields.Char(string='Attendee Name')
    attendee_email = fields.Char(string='Attendee Email')
    ticket_type = fields.Selection([
        ('standard', 'Standard'),
        ('vip', 'VIP'),
        ('sponsor', 'Sponsor'),
        ('free', 'Free'),
    ], string='Ticket Type', default='standard')
    price_unit = fields.Monetary(string='Price', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    check_in_date = fields.Datetime(string='Check-in Date', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.event.registration')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_events.group_sf_events_manager'):
            raise UserError(_('Only an event manager can perform this action.'))

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft registrations can be confirmed.'))
        if self.event_id.state == 'cancelled':
            raise UserError(_('A registration cannot be confirmed on a cancelled event.'))
        self._check_capacity()
        self.state = 'confirmed'

    def action_check_in(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed registrations can be checked in.'))
        if self.event_id.state not in ('in_progress', 'done'):
            raise UserError(_('Check-in is only possible when the event is in progress or done.'))
        self.state = 'checked_in'
        self.check_in_date = fields.Datetime.now()

    def action_done(self):
        self.ensure_one()
        if self.state not in ('confirmed', 'checked_in'):
            raise UserError(_('Only confirmed or checked-in registrations can be marked as done.'))
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state in ('checked_in', 'done'):
            raise UserError(_('A checked-in or completed participant cannot be cancelled.'))
        if self.state == 'confirmed':
            self._check_manager()
        self.state = 'cancelled'

    def _check_capacity(self):
        self.ensure_one()
        for session in self.session_ids:
            confirmed = self.env['sf.event.registration'].search([
                ('id', '!=', self.id),
                ('session_ids', 'in', session.id),
                ('state', 'in', ('confirmed', 'checked_in', 'done')),
            ])
            if session.capacity and len(confirmed) >= session.capacity:
                raise UserError(_('Session %s is full.') % session.name)
        total = self.env['sf.event.registration'].search([
            ('id', '!=', self.id),
            ('event_id', '=', self.event_id.id),
            ('state', 'in', ('confirmed', 'checked_in', 'done')),
        ])
        if self.event_id.capacity and len(total) >= self.event_id.capacity:
            raise UserError(_('Event %s has reached its capacity.') % self.event_id.name)