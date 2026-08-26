# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfMedicalAppointment(models.Model):
    _name = 'sf.medical.appointment'
    _description = 'Medical Appointment'
    _order = 'date desc, start_time'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True, copy=False)
    patient_id = fields.Many2one('sf.medical.patient', string='Patient',
                                 required=True, ondelete='restrict',
                                 index=True)
    practitioner_id = fields.Many2one('res.users', string='Practitioner',
                                      required=True, ondelete='restrict',
                                      index=True)
    date = fields.Date(string='Date', required=True, index=True)
    start_time = fields.Float(string='Start time', required=True)
    duration = fields.Float(string='Duration (hours)', required=True,
                            default=0.5)
    reason = fields.Char(string='Reason')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.medical.appointment')
        records = super().create(vals_list)
        records._check_overlap()
        return records

    def _check_overlap(self):
        for appointment in self:
            if not (appointment.practitioner_id and appointment.date
                    and appointment.start_time and appointment.duration):
                continue
            domain = [
                ('id', '!=', appointment.id),
                ('practitioner_id', '=', appointment.practitioner_id.id),
                ('date', '=', appointment.date),
                ('state', '!=', 'cancelled'),
            ]
            others = self.search(domain)
            for other in others:
                if (appointment.start_time
                        < other.start_time + other.duration
                        and other.start_time
                        < appointment.start_time + appointment.duration):
                    raise UserError(_(
                        'The practitioner already has an appointment on %s '
                        'starting at %s overlapping with this one.')
                        % (appointment.date, appointment.start_time))

    def action_schedule(self):
        for appointment in self:
            if appointment.state != 'draft':
                raise UserError(_('Only draft appointments can be '
                                  'scheduled.'))
            appointment.state = 'scheduled'

    def action_confirm(self):
        for appointment in self:
            if appointment.state not in ('draft', 'scheduled'):
                raise UserError(_('Only draft or scheduled appointments can '
                                  'be confirmed.'))
        self._check_overlap()
        self.state = 'confirmed'

    def action_done(self):
        for appointment in self:
            if appointment.state != 'confirmed':
                raise UserError(_('Only confirmed appointments can be marked '
                                  'as done.'))
            appointment.state = 'done'

    def action_cancel(self):
        for appointment in self:
            if appointment.state in ('done', 'cancelled'):
                raise UserError(_('This appointment cannot be cancelled.'))
            appointment.state = 'cancelled'

    def _check_appointment_reminders(self):
        todo = self.env.ref('mail.mail_activity_data_todo')
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            limit_date = today + timedelta(days=company.sf_medical_alert_days)
            appointments = self.with_company(company).search([
                ('state', 'in', ('scheduled', 'confirmed')),
                ('date', '<=', limit_date),
            ])
            for appointment in appointments:
                existing = appointment.activity_ids.filtered(
                    lambda activity: activity.activity_type_id == todo)
                if existing:
                    continue
                appointment.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Appointment reminder: %s') % appointment.name,
                    date_deadline=appointment.date,
                    user_id=appointment.practitioner_id.id
                    if appointment.practitioner_id else self.env.user.id)