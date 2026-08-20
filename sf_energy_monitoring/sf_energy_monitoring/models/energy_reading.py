# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EnergyReading(models.Model):
    _name = 'sf.energy.reading'
    _description = 'Energy Meter Reading'
    _order = 'date desc'

    meter_id = fields.Many2one('sf.energy.meter', string='Meter',
                               required=True, ondelete='cascade')
    date = fields.Date(string='Reading Date', required=True)
    index_value = fields.Float(string='Index', required=True)
    meter_reset = fields.Boolean(string='Meter Reset',
                                 help='Check if the meter was reset '
                                      'to zero (new cycle)')
    consumption = fields.Float(string='Consumption',
                               compute='_compute_consumption',
                               store=True)
    cost = fields.Float(string='Cost', compute='_compute_consumption',
                        store=True)
    unit = fields.Selection([
        ('kwh', 'kWh'),
        ('m3', 'm³'),
    ], string='Unit', related='meter_id.unit', store=True)
    utility_type = fields.Selection([
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
        ('water', 'Water'),
    ], string='Utility', related='meter_id.utility_type', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
    ], string='Status', default='draft')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By')
    notes = fields.Text(string='Notes')

    @api.depends('index_value', 'meter_reset', 'meter_id.reading_ids',
                 'meter_id.price_unit', 'state')
    def _compute_consumption(self):
        for reading in self:
            previous = self._get_previous_reading(reading)
            if reading.meter_reset or not previous:
                reading.consumption = reading.index_value
            else:
                reading.consumption = reading.index_value - \
                    previous.index_value
            reading.cost = round(
                reading.consumption * reading.meter_id.price_unit, 2)

    def _get_previous_reading(self, reading):
        return self.env['sf.energy.reading'].search([
            ('meter_id', '=', reading.meter_id.id),
            ('date', '<', reading.date),
            ('state', '=', 'confirmed'),
        ], order='date desc', limit=1)

    @api.constrains('index_value', 'meter_reset')
    def _check_index(self):
        for reading in self:
            if reading.index_value < 0:
                raise UserError(_('The index cannot be negative.'))
            previous = self._get_previous_reading(reading)
            if previous and not reading.meter_reset \
                    and reading.index_value < previous.index_value:
                raise UserError(
                    _('The index cannot be lower than the previous '
                      'reading (%s) unless the meter was reset. '
                      'Tick "Meter Reset" if the meter was zeroed.')
                    % previous.index_value)

    @api.constrains('meter_id', 'date')
    def _check_unique_date(self):
        for reading in self:
            duplicate = self.env['sf.energy.reading'].search([
                ('meter_id', '=', reading.meter_id.id),
                ('date', '=', reading.date),
                ('id', '!=', reading.id),
            ])
            if duplicate:
                raise UserError(
                    _('A reading already exists for this meter on '
                      '%s.') % reading.date)

    def action_confirm(self):
        for reading in self:
            if reading.state != 'draft':
                raise UserError(
                    _('Only draft readings can be confirmed.'))
            reading.write({
                'state': 'confirmed',
                'confirmed_by': self.env.user.id,
            })

    def action_to_draft(self):
        for reading in self:
            if reading.state != 'confirmed':
                raise UserError(
                    _('Only confirmed readings can be returned to draft.'))
            reading.write({'state': 'draft', 'confirmed_by': False})

    def write(self, vals):
        for reading in self:
            if reading.state == 'confirmed' and \
                    any(f in vals for f in ('index_value', 'date',
                                            'meter_id', 'meter_reset')):
                raise UserError(
                    _('A confirmed reading cannot be modified. '
                      'Return it to draft first.'))
        return super().write(vals)