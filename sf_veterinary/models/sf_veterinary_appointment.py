# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfVeterinaryAppointment(models.Model):
    _name = 'sf.veterinary.appointment'
    _description = 'Veterinary Appointment'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    patient_id = fields.Many2one(
        'sf.veterinary.patient', string='Patient', ondelete='restrict',
        required=True, index=True, tracking=True)
    owner_id = fields.Many2one(
        'res.partner', string='Owner', related='patient_id.owner_id',
        store=True, readonly=True, index=True)
    veterinarian_id = fields.Many2one(
        'res.partner', string='Veterinarian', ondelete='set null',
        domain="[('sf_veterinary_is_veterinarian', '=', True)]",
        tracking=True)
    start_datetime = fields.Datetime(
        string='Start', default=lambda self: fields.Datetime.now() +
        timedelta(hours=1), tracking=True)
    duration_minutes = fields.Integer(
        string='Duration (minutes)',
        default=lambda self: self.env.company.sf_veterinary_default_duration_minutes or 30,
        tracking=True)
    end_datetime = fields.Datetime(
        string='End', compute='_compute_end_datetime', store=True,
        readonly=True)
    motif = fields.Selection([
        ('checkup', 'Check-up'),
        ('consultation', 'Consultation'),
        ('vaccination', 'Vaccination'),
        ('surgery', 'Surgery'),
        ('followup', 'Follow-up'),
        ('other', 'Other'),
    ], string='Reason', default='consultation', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.depends('start_datetime', 'duration_minutes')
    def _compute_end_datetime(self):
        for appointment in self:
            if appointment.start_datetime and appointment.duration_minutes:
                appointment.end_datetime = appointment.start_datetime + \
                    timedelta(minutes=appointment.duration_minutes)
            else:
                appointment.end_datetime = appointment.start_datetime

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.veterinary.appointment')
        if vals.get('start_datetime'):
            start = fields.Datetime.to_datetime(vals['start_datetime'])
            if start < fields.Datetime.now():
                raise UserError(_('Appointments cannot be scheduled in the '
                                  'past.'))
        return super().create(vals)

    def write(self, vals):
        if vals.get('start_datetime'):
            start = fields.Datetime.to_datetime(vals['start_datetime'])
            if start < fields.Datetime.now():
                raise UserError(_('Appointments cannot be scheduled in the '
                                  'past.'))
        return super().write(vals)

    def action_confirm(self):
        for appointment in self:
            if appointment.state != 'draft':
                raise UserError(_('Only draft appointments can be confirmed.'))
        self.state = 'confirm'

    def action_done(self):
        for appointment in self:
            if appointment.state != 'confirm':
                raise UserError(_('Only confirmed appointments can be marked '
                                  'as done.'))
        self.state = 'done'

    def action_cancel(self):
        for appointment in self:
            if appointment.state not in ('draft', 'confirm'):
                raise UserError(_('Only draft or confirmed appointments can '
                                  'be cancelled.'))
        self.state = 'cancelled'
