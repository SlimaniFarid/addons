# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfSalonAppointment(models.Model):
    _name = 'sf.salon.appointment'
    _description = 'Salon Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.salon.activity.mixin']
    _order = 'start_datetime desc, id desc'

    _FINAL_STATES = ('done', 'cancelled', 'no_show')
    _IMMUTABLE_FIELDS = ('partner_id', 'staff_id', 'service_id', 'start_datetime', 'package_id')
    _STATE_TRANSITIONS = {
        'draft': ('confirmed', 'cancelled'),
        'confirmed': ('in_progress', 'cancelled', 'no_show'),
        'in_progress': ('done', 'cancelled', 'no_show'),
        'done': (),
        'cancelled': (),
        'no_show': (),
    }

    name = fields.Char(string='Name', required=True, copy=False)
    partner_id = fields.Many2one('res.partner', string='Customer', required=True, ondelete='restrict')
    staff_id = fields.Many2one('sf.salon.staff', string='Staff', required=True, ondelete='restrict')
    service_id = fields.Many2one('sf.salon.service', string='Service', required=True, ondelete='restrict')
    start_datetime = fields.Datetime(string='Start', required=True)
    duration = fields.Integer(string='Duration (Minutes)', compute='_compute_duration', store=True)
    end_datetime = fields.Datetime(string='End', compute='_compute_duration', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ], string='Status', default='draft', copy=False)
    package_id = fields.Many2one('sf.salon.package', string='Package', ondelete='set null')
    invoice_id = fields.Many2one('account.move', string='Invoice', ondelete='set null')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('service_id.duration', 'start_datetime')
    def _compute_duration(self):
        for appointment in self:
            duration = appointment.service_id.duration or 0
            appointment.duration = duration
            if appointment.start_datetime:
                appointment.end_datetime = appointment.start_datetime + timedelta(minutes=duration)
            else:
                appointment.end_datetime = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.salon.appointment')
            if vals.get('state', 'draft') != 'draft':
                raise UserError(_('Appointments must be created in draft state. Use the workflow buttons to change the status.'))
        return super().create(vals_list)

    def write(self, vals):
        for rec in self:
            if rec.state in self._FINAL_STATES and any(f in vals for f in self._IMMUTABLE_FIELDS):
                raise UserError(_('This appointment is final and its business fields cannot be modified.'))
            if 'state' in vals and vals['state'] != rec.state and vals['state'] not in self._STATE_TRANSITIONS.get(rec.state, ()):
                raise UserError(_('Invalid state transition from %s to %s. Use the workflow buttons.') % (rec.state, vals['state']))
            if vals.get('state') == 'confirmed':
                rec._check_conflict(rec.start_datetime, rec.end_datetime, rec.staff_id.id, exclude_id=rec.id)
        return super().write(vals)

    def _check_conflict(self, start, end, staff_id, exclude_id=None):
        domain = [
            ('staff_id', '=', staff_id),
            ('state', 'in', ('confirmed', 'in_progress')),
            ('start_datetime', '<', end),
        ]
        if exclude_id:
            domain.append(('id', '!=', exclude_id))
        conflicts = self.search(domain).filtered(lambda a: a.end_datetime > start)
        if conflicts:
            raise UserError(_('The staff member is already booked for another appointment during this period.'))

    def action_confirm(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft appointments can be confirmed.'))
        if not self.start_datetime:
            raise UserError(_('Set a start datetime before confirming.'))
        self._check_conflict(self.start_datetime, self.end_datetime, self.staff_id.id)
        self.state = 'confirmed'

    def action_start(self):
        self.ensure_one()
        if self.state != 'confirmed':
            raise UserError(_('Only confirmed appointments can be started.'))
        self.state = 'in_progress'

    def action_done(self):
        self.ensure_one()
        if self.state != 'in_progress':
            raise UserError(_('Only in-progress appointments can be completed.'))
        if self.package_id:
            if self.package_id.partner_id.id != self.partner_id.id:
                raise UserError(_('The package belongs to another customer.'))
            if self.package_id.service_id.id != self.service_id.id:
                raise UserError(_('The package is not valid for this service.'))
            if self.package_id.state in ('refunded', 'expired', 'exhausted'):
                raise UserError(_('The package is %s and can no longer be used for this appointment.') % self.package_id.state)
            self.package_id._consume_session()
        else:
            self._create_invoice()
        self.state = 'done'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'done':
            raise UserError(_('A done appointment cannot be cancelled.'))
        self.state = 'cancelled'

    def action_no_show(self):
        self.ensure_one()
        if self.state not in ('confirmed', 'in_progress'):
            raise UserError(_('Only confirmed or in-progress appointments can be marked as no show.'))
        self.state = 'no_show'

    def _create_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            return self.invoice_id
        product = self.service_id.product_id
        if not product:
            raise UserError(_('The service "%s" has no invoice product configured. Set the product on the service before completing appointments.') % self.service_id.name)
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': product.id,
                'name': self.service_id.name,
                'quantity': 1,
                'price_unit': self.service_id.price,
            })],
        })
        self.invoice_id = invoice.id
        return invoice