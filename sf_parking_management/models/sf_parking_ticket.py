# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfParkingTicket(models.Model):
    _name = 'sf.parking.ticket'
    _description = 'Parking Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.parking.activity.mixin']
    _order = 'entry_datetime desc, id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    site_id = fields.Many2one('sf.parking.site', string='Site', required=True, ondelete='restrict')
    place_id = fields.Many2one('sf.parking.place', string='Place', ondelete='set null',
                               domain="[('zone_id.site_id', '=', site_id), ('state', 'in', ('free', 'occupied'))]")
    vehicle_plate = fields.Char(string='Vehicle Plate')
    entry_datetime = fields.Datetime(string='Entry', default=fields.Datetime.now)
    exit_datetime = fields.Datetime(string='Exit')
    duration = fields.Float(string='Duration (Hours)', compute='_compute_duration', store=True)
    amount = fields.Monetary(string='Amount', compute='_compute_amount', store=True, currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', copy=False)
    subscription_id = fields.Many2one('sf.parking.subscription', string='Subscription', ondelete='set null')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    _sql_constraints = [
        ('check_exit_after_entry',
         'CHECK (exit_datetime IS NULL OR entry_datetime IS NULL OR exit_datetime >= entry_datetime)',
         'The exit datetime cannot be before the entry datetime.'),
    ]

    @api.depends('entry_datetime', 'exit_datetime')
    def _compute_duration(self):
        for ticket in self:
            if ticket.entry_datetime and ticket.exit_datetime:
                ticket.duration = max(
                    0.0, (ticket.exit_datetime - ticket.entry_datetime).total_seconds() / 3600.0)
            else:
                ticket.duration = 0.0

    @api.depends('duration', 'site_id', 'subscription_id',
                 'site_id.hourly_rate', 'site_id.daily_rate', 'subscription_id.state')
    def _compute_amount(self):
        for ticket in self:
            if ticket.subscription_id and ticket.subscription_id.state in ('active', 'renewed'):
                ticket.amount = 0.0
                continue
            hourly = ticket.site_id.hourly_rate or 0.0
            daily = ticket.site_id.daily_rate or 0.0
            if daily:
                days = int(ticket.duration // 24)
                rest = ticket.duration - days * 24
                ticket.amount = days * daily + min(rest * hourly, daily)
            else:
                ticket.amount = ticket.duration * hourly

    @api.constrains('entry_datetime', 'exit_datetime')
    def _check_exit_after_entry(self):
        for ticket in self:
            if ticket.entry_datetime and ticket.exit_datetime and ticket.exit_datetime < ticket.entry_datetime:
                raise ValidationError(_('The exit datetime cannot be before the entry datetime.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.parking.ticket')
            if vals.get('place_id'):
                self._check_place_valid(vals['place_id'], vals.get('site_id'))
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_parking_management.group_sf_parking_manager'):
            raise UserError(_('Only a parking manager can perform this action.'))

    def _check_place_valid(self, place_id, site_id):
        place = self.env['sf.parking.place'].browse(place_id)
        if not place:
            return
        if site_id and place.zone_id.site_id.id != site_id:
            raise UserError(_('The place does not belong to the selected site.'))
        if place.state == 'out_of_service':
            raise UserError(_('An out-of-service place cannot receive a ticket.'))

    def _release_place(self):
        for ticket in self:
            if ticket.place_id and ticket.place_id.state == 'occupied':
                ticket.place_id.state = 'free'

    def action_open(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft tickets can be opened.'))
        if self.place_id:
            if self.place_id.state != 'free':
                raise UserError(_('The place is not free (occupied, reserved or out of service).'))
            self.place_id.state = 'occupied'
        self.state = 'open'

    def action_close(self):
        self.ensure_one()
        if self.state != 'open':
            raise UserError(_('Only open tickets can be closed.'))
        if self.exit_datetime and self.entry_datetime and self.exit_datetime < self.entry_datetime:
            raise UserError(_('The exit datetime cannot be before the entry datetime.'))
        if not self.exit_datetime:
            self.exit_datetime = fields.Datetime.now()
        self.state = 'closed'
        self._release_place()

    def action_paid(self):
        self.ensure_one()
        if self.state != 'closed':
            raise UserError(_('Only closed tickets can be marked paid.'))
        self.state = 'paid'

    def action_cancel(self):
        self.ensure_one()
        if self.state == 'paid':
            raise UserError(_('A paid ticket cannot be cancelled.'))
        self._check_manager()
        self._release_place()
        self.state = 'cancelled'