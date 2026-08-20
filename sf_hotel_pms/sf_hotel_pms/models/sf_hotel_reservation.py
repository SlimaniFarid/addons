# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SfHotelReservation(models.Model):
    _name = 'sf.hotel.reservation'
    _description = 'Hotel Reservation'
    _order = 'check_in desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    guest_id = fields.Many2one('res.partner', string='Guest',
                               ondelete='restrict')
    guest_name = fields.Char(string='Guest name', index=True)
    check_in = fields.Date(string='Check-in', required=True, tracking=True)
    check_out = fields.Date(string='Check-out', required=True, tracking=True)
    room_ids = fields.Many2many('sf.hotel.room', string='Rooms',
                                tracking=True)
    guest_count = fields.Integer(string='Guests', default=1)
    nights = fields.Integer(string='Nights', compute='_compute_nights',
                            store=True)
    total = fields.Float(string='Stay total', compute='_compute_total',
                         store=True)
    extra_ids = fields.One2many('sf.hotel.extra', 'reservation_id',
                                string='Extras')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('check_in', 'check_out')
    def _compute_nights(self):
        for reservation in self:
            if reservation.check_in and reservation.check_out:
                reservation.nights = (reservation.check_out
                                      - reservation.check_in).days
            else:
                reservation.nights = 0

    @api.depends('nights', 'room_ids.base_price',
                 'extra_ids.state', 'extra_ids.amount')
    def _compute_total(self):
        for reservation in self:
            rooms_total = (sum(reservation.room_ids.mapped('base_price'))
                           * reservation.nights)
            extras_total = sum(reservation.extra_ids.filtered(
                lambda extra: extra.state == 'charged').mapped('amount'))
            reservation.total = rooms_total + extras_total

    @api.constrains('check_in', 'check_out')
    def _check_dates(self):
        for reservation in self:
            if reservation.check_in and reservation.check_out and \
                    reservation.check_out <= reservation.check_in:
                raise ValidationError(_('Check-out must be after check-in.'))

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.hotel.reservation')
        return super().create(vals)

    def _check_manager(self):
        if not self.env.user.has_group('sf_hotel_pms.group_sf_hotel_manager'):
            raise UserError(_('Only hotel managers can perform this '
                              'operation.'))

    def action_reservation_confirm(self):
        self.ensure_one()
        if self.status != 'draft':
            raise UserError(_('Only draft reservations can be confirmed.'))
        for room in self.room_ids:
            overlapping = self.search([
                ('id', '!=', self.id),
                ('status', 'in', ['confirmed', 'checked_in']),
                ('room_ids', 'in', room.id),
                ('check_in', '<', self.check_out),
                ('check_out', '>', self.check_in),
            ])
            if overlapping:
                raise UserError(_('Room %s is already booked for this '
                                  'period.') % room.name)
        self.room_ids.write({'status': 'reserved'})
        self.status = 'confirmed'

    def action_check_in(self):
        self.ensure_one()
        self._check_manager()
        if self.status != 'confirmed':
            raise UserError(_('Only confirmed reservations can be checked '
                              'in.'))
        self.room_ids.write({'status': 'occupied'})
        self.status = 'checked_in'

    def action_check_out(self):
        self.ensure_one()
        self._check_manager()
        if self.status != 'checked_in':
            raise UserError(_('Only checked-in reservations can be checked '
                              'out.'))
        self.room_ids.write({'status': 'available'})
        self.status = 'checked_out'

    def action_cancel(self):
        self.ensure_one()
        if self.status in ('checked_in', 'checked_out'):
            raise UserError(_('Checked-in or checked-out reservations '
                              'cannot be cancelled.'))
        self.room_ids.write({'status': 'available'})
        self.status = 'cancelled'

    def _check_departures_and_housekeeping(self):
        companies = self.env['res.company'].search([])
        for company in companies:
            today = fields.Date.context_today(self.with_company(company))
            reservations = self.with_company(company).search([
                ('status', '=', 'confirmed'),
                ('check_out', '=', today),
            ])
            todo_type = self.env.ref('mail.mail_activity_data_todo')
            for reservation in reservations:
                existing = reservation.activity_ids.filtered(
                    lambda activity: activity.activity_type_id == todo_type)
                if not existing:
                    reservation.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Departure today: %s')
                        % (reservation.guest_name or reservation.name),
                        user_id=self.env.user.id)
            rooms = self.env['sf.hotel.room'].with_company(company).search([
                ('status', '=', 'occupied'),
            ])
            tomorrow = today + timedelta(days=1)
            for room in rooms:
                planned = self.env['sf.hotel.housekeeping'].with_company(
                    company).search([
                        ('room_id', '=', room.id),
                        ('date', '=', tomorrow),
                    ])
                existing = room.activity_ids.filtered(
                    lambda activity: activity.activity_type_id == todo_type)
                if not planned and not existing:
                    room.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Housekeeping needed tomorrow: %s')
                        % room.name,
                        user_id=self.env.user.id)
