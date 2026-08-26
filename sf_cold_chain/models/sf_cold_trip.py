# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfColdTrip(models.Model):
    _name = 'sf.cold.trip'
    _description = 'Cold Transport Trip'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.cold.chain.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    origin = fields.Char(string='Origin', required=True)
    destination = fields.Char(string='Destination', required=True)
    vehicle_plate = fields.Char(string='Vehicle Plate')
    driver_name = fields.Char(string='Driver Name')
    target_min_temp = fields.Float(string='Target Min Temp', required=True,
                                   default=2.0)
    target_max_temp = fields.Float(string='Target Max Temp', required=True,
                                   default=8.0)
    departure_datetime = fields.Datetime(string='Departure Datetime')
    arrival_datetime = fields.Datetime(string='Arrival Datetime')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned', copy=False)
    reading_ids = fields.One2many('sf.cold.reading', 'trip_id', string='Readings')
    excursion_ids = fields.One2many('sf.cold.excursion', 'trip_id', string='Excursions')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.constrains('target_min_temp', 'target_max_temp')
    def _check_temperature_range(self):
        for trip in self:
            if trip.target_max_temp < trip.target_min_temp:
                raise ValidationError(_(
                    'The maximum temperature cannot be lower than the minimum temperature.'))
            if (trip.arrival_datetime and trip.departure_datetime
                    and trip.arrival_datetime < trip.departure_datetime):
                raise ValidationError(_(
                    'The arrival datetime cannot be before the departure datetime.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.cold.trip')
        return super().create(vals_list)

    def _check_manager(self):
        if not self.env.user.has_group('sf_cold_chain.group_sf_cold_chain_manager'):
            raise UserError(_('Only a cold chain manager can perform this action.'))

    def action_start(self):
        self.ensure_one()
        if self.state != 'planned':
            raise UserError(_('Only planned trips can be started.'))
        self.write({
            'state': 'in_transit',
            'departure_datetime': self.departure_datetime or fields.Datetime.now(),
        })

    def action_complete(self):
        self.ensure_one()
        if self.state != 'in_transit':
            raise UserError(_('Only in-transit trips can be completed.'))
        arrival = self.arrival_datetime or fields.Datetime.now()
        if arrival < self.departure_datetime:
            raise UserError(_('The arrival datetime cannot be before the departure datetime.'))
        self.write({
            'state': 'completed',
            'arrival_datetime': arrival,
        })

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state in ('completed', 'cancelled'):
            raise UserError(_('A completed or cancelled trip cannot be cancelled.'))
        self.state = 'cancelled'

# --- business booster (auto) ---
class _Boost(models.Model):
    _inherit = 'sf.cold.chain.activity.mixin'

    active = fields.Boolean(string='Active', default=True)
    user_id = fields.Many2one(
        'res.users', string='Responsible', tracking=True,
        index=True, default=lambda self: self.env.user,
        help='Internal owner responsible for this record.')
