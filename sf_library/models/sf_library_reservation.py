# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLibraryReservation(models.Model):
    _name = 'sf.library.reservation'
    _description = 'Library Reservation'
    _order = 'id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    item_id = fields.Many2one(
        'sf.library.item', string='Item', ondelete='restrict',
        index=True, required=True, tracking=True)
    member_id = fields.Many2one(
        'sf.library.member', string='Member', ondelete='restrict',
        index=True, required=True, tracking=True)
    reservation_date = fields.Date(
        string='Reservation date', default=fields.Date.context_today,
        tracking=True)
    expiry_date = fields.Date(string='Expiry date')
    status = fields.Selection([
        ('waiting', 'Waiting'),
        ('ready', 'Ready'),
        ('fulfilled', 'Fulfilled'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='waiting', required=True, tracking=True,
       index=True)
    company_id = fields.Many2one(
        'res.company', string='Company',
        default=lambda self: self.env.company, required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.library.reservation')
        reservation = super().create(vals)
        reservation._process_ready_reservations()
        return reservation

    def _process_ready_reservations(self):
        for company in self.env['res.company'].search([]):
            today = fields.Date.context_today(self.with_company(company))
            reservations = self.with_company(company).search([
                ('status', '=', 'waiting'),
            ])
            for reservation in reservations:
                if reservation.item_id.available_copies >= 1:
                    reservation.status = 'ready'
                    reservation.expiry_date = today + timedelta(
                        days=company.sf_library_hold_days)

    def action_check_availability(self):
        self._process_ready_reservations()

    def action_fulfil(self):
        if not self.env.user.has_group('sf_library.group_sf_library_manager'):
            raise UserError(_('Only a library manager can fulfil a '
                              'reservation.'))
        for reservation in self:
            if reservation.status != 'ready':
                raise UserError(_('Only ready reservations can be fulfilled.'))
        self.status = 'fulfilled'

    def action_cancel(self):
        if not self.env.user.has_group('sf_library.group_sf_library_manager'):
            raise UserError(_('Only a library manager can cancel a '
                              'reservation.'))
        for reservation in self:
            if reservation.status not in ('waiting', 'ready'):
                raise UserError(_('Only waiting or ready reservations can be '
                                  'cancelled.'))
        self.status = 'cancelled'
