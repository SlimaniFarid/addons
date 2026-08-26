# -*- coding: utf-8 -*-
"""Facility management models."""
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SfFacilitySite(models.Model):
    _name = 'sf.facility.site'
    _description = 'Facility Site'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Site Name', required=True)
    company_id = fields.Many2one('res.company', required=True,
                                 default=lambda s: s.env.company)
    address = fields.Text(string='Address')
    surface_m2 = fields.Float(string='Surface (m2)')
    lease_reference = fields.Char(string='Lease Reference')
    owner_type = fields.Selection([
        ('owned', 'Owned'), ('leased', 'Leased')], default='leased')
    room_ids = fields.One2many('sf.facility.room', 'site_id',
                               string='Rooms')
    room_count = fields.Integer(compute='_compute_room_count')

    def _compute_room_count(self):
        for rec in self:
            rec.room_count = len(rec.room_ids)


class SfFacilityRoom(models.Model):
    _name = 'sf.facility.room'
    _description = 'Facility Room'

    name = fields.Char(string='Room Name', required=True)
    site_id = fields.Many2one('sf.facility.site', string='Site', required=True,
                              ondelete='cascade')
    company_id = fields.Many2one(related='site_id.company_id', store=True)
    room_type = fields.Selection([
        ('office', 'Office'), ('meeting', 'Meeting Room'),
        ('storage', 'Storage'), ('production', 'Production'),
        ('lab', 'Laboratory'), ('other', 'Other')], default='office')
    capacity = fields.Integer(string='Capacity (people)')
    floor = fields.Char(string='Floor')
    surface_m2 = fields.Float(string='Surface (m2)')
    booking_ids = fields.One2many('sf.facility.booking', 'room_id',
                                  string='Bookings')


class SfFacilityBooking(models.Model):
    _name = 'sf.facility.booking'
    _description = 'Facility Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Booking Reference', required=True, copy=False,
                       readonly=True, default='New')
    room_id = fields.Many2one('sf.facility.room', string='Room', required=True)
    company_id = fields.Many2one(related='room_id.company_id', store=True)
    booked_by_id = fields.Many2one('res.users', string='Booked By',
                                   default=lambda s: s.env.uid)
    purpose = fields.Char(string='Purpose', required=True)
    start = fields.Datetime(string='Start', required=True)
    end = fields.Datetime(string='End', required=True)
    attendees = fields.Integer(string='Attendees')
    state = fields.Selection([
        ('booked', 'Booked'), ('cancelled', 'Cancelled')],
        default='booked', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code(
                    'sf.facility.booking') or 'FBK-NEW'
        return super().create(vals_list)

    @api.constrains('start', 'end')
    def _check_times(self):
        for rec in self:
            if rec.end <= rec.start:
                raise ValidationError(_('End must be after start.'))
            if rec.state != 'booked':
                continue
            conflict = self.search([
                ('id', '!=', rec.id), ('room_id', '=', rec.room_id.id),
                ('state', '=', 'booked'), ('start', '<', rec.end),
                ('end', '>', rec.start)], limit=1)
            if conflict:
                raise ValidationError(_(
                    'Room %s is already booked from %s to %s (%s).')
                    % (rec.room_id.name, conflict.start, conflict.end,
                       conflict.name))

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.facility.site'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
