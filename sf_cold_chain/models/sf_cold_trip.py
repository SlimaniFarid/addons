# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class SfColdTrip(models.Model):
    _name = 'sf.cold.trip'
    _description = 'Cold Transport Trip'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.cold.chain.activity.mixin']
    _order = 'id desc'

    name = fields.Char(string='Name', required=True, copy=False)
    carrier_id = fields.Many2one('res.partner', string='Carrier', required=True,
                                 ondelete='restrict')
    vehicle_plate = fields.Char(string='Vehicle Plate')
    cargo_description = fields.Char(string='Cargo')
    temperature_min = fields.Float(string='Min Temperature', required=True,
                                   default=2.0)
    temperature_max = fields.Float(string='Max Temperature', required=True,
                                   default=8.0)
    planned_departure = fields.Datetime(string='Planned Departure')
    planned_arrival = fields.Datetime(string='Planned Arrival')
    actual_departure = fields.Datetime(string='Actual Departure')
    actual_arrival = fields.Datetime(string='Actual Arrival')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_transit', 'In Transit'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned', copy=False)
    reading_ids = fields.One2many('sf.cold.reading', 'trip_id',
                                  string='Readings')
    excursion_ids = fields.One2many('sf.cold.excursion', 'trip_id',
                                    string='Excursions')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.constrains('temperature_min', 'temperature_max')
    def _check_temperature_range(self):
        for trip in self:
            if trip.temperature_max < trip.temperature_min:
                raise ValidationError(_(
                    'The maximum temperature cannot be lower than the minimum temperature.'))
            if (trip.actual_arrival and trip.actual_departure
                    and trip.actual_arrival < trip.actual_departure):
                raise ValidationError(_(
                    'The actual arrival time cannot be before the actual departure time.'))

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
            'actual_departure': self.actual_departure or fields.Datetime.now(),
        })

    def action_complete(self):
        self.ensure_one()
        if self.state != 'in_transit':
            raise UserError(_('Only in-transit trips can be completed.'))
        arrival = self.actual_arrival or fields.Datetime.now()
        if arrival < self.actual_departure:
            raise UserError(_('The actual arrival time cannot be before the actual departure time.'))
        self.write({
            'state': 'completed',
            'actual_arrival': arrival,
        })

    def action_cancel(self):
        self.ensure_one()
        self._check_manager()
        if self.state in ('completed', 'cancelled'):
            raise UserError(_('A completed or cancelled trip cannot be cancelled.'))
        self.state = 'cancelled'