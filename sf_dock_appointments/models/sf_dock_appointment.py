# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfDockAppointment(models.Model):
    _name = 'sf.dock.appointment'
    _description = 'Dock Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.dock.appointments.activity.mixin']
    _order = 'appointment_datetime asc, id asc'

    name = fields.Char(string='Name', required=True, copy=False)
    dock_id = fields.Many2one('sf.dock', string='Dock', required=True,
                              ondelete='restrict')
    partner_id = fields.Many2one('res.partner', string='Carrier', required=True,
                                 ondelete='restrict')
    direction = fields.Selection([
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
    ], string='Direction', required=True, default='inbound')
    reference = fields.Char(string='Reference')
    appointment_datetime = fields.Datetime(string='Appointment', required=True,
                                           index=True)
    window_minutes = fields.Integer(string='Window (Minutes)', required=True,
                                    default=60)
    carrier_name = fields.Char(string='Carrier Name')
    vehicle_plate = fields.Char(string='Vehicle Plate')
    driver_name = fields.Char(string='Driver Name')
    state = fields.Selection([
        ('scheduled', 'Scheduled'),
        ('arrived', 'Arrived'),
        ('docked', 'Docked'),
        ('completed', 'Completed'),
        ('no_show', 'No-Show'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='scheduled', copy=False)
    actual_arrival_datetime = fields.Datetime(string='Actual Arrival')
    actual_dock_datetime = fields.Datetime(string='Actual Dock')
    actual_departure_datetime = fields.Datetime(string='Actual Departure')
    delay_minutes = fields.Integer(string='Delay (Minutes)',
                                   compute='_compute_durations', store=True)
    dock_duration_minutes = fields.Integer(string='Dock Duration (Minutes)',
                                           compute='_compute_durations', store=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company, index=True)

    _sql_constraints = [
        ('check_window_positive',
         'CHECK (window_minutes > 0)',
         'The appointment window must be greater than zero minutes.'),
    ]

    @api.constrains('window_minutes')
    def _check_window(self):
        for appointment in self:
            if appointment.window_minutes <= 0:
                raise ValidationError(_('The appointment window must be greater than zero minutes.'))

    @api.depends('actual_arrival_datetime', 'actual_dock_datetime',
                 'actual_departure_datetime', 'appointment_datetime', 'window_minutes')
    def _compute_durations(self):
        for appointment in self:
            if appointment.actual_departure_datetime and appointment.appointment_datetime:
                window_end = appointment.appointment_datetime + timedelta(
                    minutes=appointment.window_minutes / 2.0)
                delay = appointment.actual_departure_datetime - window_end
                appointment.delay_minutes = int(max(0, delay.total_seconds() // 60))
            else:
                appointment.delay_minutes = 0
            if (appointment.actual_departure_datetime
                    and appointment.actual_dock_datetime):
                duration = appointment.actual_departure_datetime - appointment.actual_dock_datetime
                appointment.dock_duration_minutes = int(max(0, duration.total_seconds() // 60))
            else:
                appointment.dock_duration_minutes = 0

    def _default_window(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_dock_appointments.default_window_minutes')
        return int(param) if param else 60

    @api.model
    def _window_bounds(self, appointment_datetime, window_minutes):
        half = timedelta(minutes=window_minutes / 2.0)
        return appointment_datetime - half, appointment_datetime + half

    def _check_overlap(self, dock_id, appointment_datetime, window_minutes,
                       exclude_id=None):
        if not appointment_datetime:
            return
        start, end = self._window_bounds(appointment_datetime, window_minutes)
        domain = [
            ('dock_id', '=', dock_id),
            ('state', 'in', ('scheduled', 'arrived', 'docked')),
        ]
        if exclude_id:
            domain.append(('id', '!=', exclude_id))
        others = self.search(domain)
        for other in others:
            o_start, o_end = self._window_bounds(
                other.appointment_datetime, other.window_minutes)
            if start < o_end and o_start < end:
                raise UserError(_(
                    'The appointment overlaps with %s on the same dock.') % other.name)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.dock.appointment')
            if not vals.get('window_minutes'):
                vals['window_minutes'] = self._default_window()
            self._check_overlap(vals.get('dock_id'), vals.get('appointment_datetime'),
                                vals.get('window_minutes'))
        return super().create(vals_list)

    def write(self, vals):
        for record in self:
            if any(f in vals for f in ('dock_id', 'appointment_datetime',
                                       'window_minutes')):
                self._check_overlap(
                    vals.get('dock_id', record.dock_id.id),
                    vals.get('appointment_datetime', record.appointment_datetime),
                    vals.get('window_minutes', record.window_minutes),
                    exclude_id=record.id)
        return super().write(vals)

    def _get_grace_minutes(self):
        param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_dock_appointments.grace_minutes')
        return int(param) if param else 15

    def _check_manager(self):
        if not self.env.user.has_group('sf_dock_appointments.group_sf_dock_appointments_manager'):
            raise UserError(_('Only a dock appointments manager can perform this action.'))

    def action_arrive(self):
        self.ensure_one()
        if self.state != 'scheduled':
            raise UserError(_('Only scheduled appointments can be registered as arrived.'))
        arrival = self.actual_arrival_datetime or fields.Datetime.now()
        earliest = self.appointment_datetime - timedelta(minutes=self._get_grace_minutes())
        if arrival < earliest:
            raise UserError(_(
                'Arrival time cannot be earlier than %s minutes before the appointment time.') % self._get_grace_minutes())
        self.write({
            'state': 'arrived',
            'actual_arrival_datetime': arrival,
        })

    def action_dock(self):
        self.ensure_one()
        if self.state != 'arrived':
            raise UserError(_('Only arrived appointments can be moved to dock.'))
        dock_at = self.actual_dock_datetime or fields.Datetime.now()
        if dock_at < self.actual_arrival_datetime:
            raise UserError(_('The dock time cannot be before the arrival time.'))
        self.write({
            'state': 'docked',
            'actual_dock_datetime': dock_at,
        })

    def action_complete(self):
        self.ensure_one()
        if self.state != 'docked':
            raise UserError(_('Only docked appointments can be completed.'))
        departure = self.actual_departure_datetime or fields.Datetime.now()
        if departure < self.actual_dock_datetime:
            raise UserError(_('The departure time cannot be before the dock time.'))
        self.write({
            'state': 'completed',
            'actual_departure_datetime': departure,
        })

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state in ('completed', 'no_show', 'cancelled'):
            raise UserError(_('A completed, no-show or cancelled appointment cannot be cancelled.'))
        self.state = 'cancelled'

    def _cron_daily_checks(self):
        todo_type = self.env.ref('mail.mail_activity_data_todo')
        grace_param = self.env['ir.config_parameter'].sudo().get_param(
            'sf_dock_appointments.grace_minutes')
        grace = int(grace_param) if grace_param else 15
        companies = self.env['res.company'].search([])
        now = fields.Datetime.now()
        # Pre-filter: appointment_datetime + max_window/2 + grace < now
        # Use a reasonable max window (e.g., 480 minutes) to limit search
        max_window = 480
        cutoff = now - timedelta(minutes=max_window / 2 + grace)
        for company in companies:
            scoped = self.with_company(company)
            domain = [
                ('state', '=', 'scheduled'),
                ('appointment_datetime', '<', cutoff),
            ]
            candidates = scoped.env['sf.dock.appointment'].search(domain)
            for appointment in candidates:
                _, window_end = self._window_bounds(
                    appointment.appointment_datetime, appointment.window_minutes)
                if window_end + timedelta(minutes=grace) < now:
                    appointment.state = 'no_show'
                    appointment._sf_check_todo(
                        todo_type,
                        'Appointment %s is a no-show' % appointment.name,
                        'The truck never arrived within its window. Contact the carrier.',
                    )