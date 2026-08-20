# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SfColdReading(models.Model):
    _name = 'sf.cold.reading'
    _description = 'Cold Chain Reading'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.cold.chain.activity.mixin']
    _order = 'reading_datetime asc, id asc'

    name = fields.Char(string='Name', compute='_compute_name', store=True)
    trip_id = fields.Many2one('sf.cold.trip', string='Trip', ondelete='cascade')
    site_id = fields.Many2one('sf.cold.site', string='Site', ondelete='cascade')
    reading_datetime = fields.Datetime(string='Reading Time', required=True,
                                       default=lambda self: fields.Datetime.now())
    temperature = fields.Float(string='Temperature', required=True)
    within_range = fields.Boolean(string='Within Range',
                                  compute='_compute_within_range', store=True)
    temperature_min = fields.Float(string='Min Temperature',
                                   compute='_compute_limits', store=True)
    temperature_max = fields.Float(string='Max Temperature',
                                   compute='_compute_limits', store=True)
    deviation = fields.Float(string='Deviation', compute='_compute_within_range',
                             store=True)
    excursion_id = fields.Many2one('sf.cold.excursion', string='Excursion',
                                   ondelete='set null')
    recorded_by = fields.Many2one('res.users', string='Recorded By',
                                  default=lambda self: self.env.user,
                                  readonly=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.constrains('trip_id', 'site_id')
    def _check_source(self):
        for reading in self:
            if not reading.trip_id and not reading.site_id:
                raise ValidationError(_(
                    'A reading must be linked to a trip or a cold storage site.'))

    @api.depends('trip_id.temperature_min', 'trip_id.temperature_max',
                 'site_id.temperature_min', 'site_id.temperature_max')
    def _compute_limits(self):
        for reading in self:
            if reading.trip_id:
                reading.temperature_min = reading.trip_id.temperature_min
                reading.temperature_max = reading.trip_id.temperature_max
            elif reading.site_id:
                reading.temperature_min = reading.site_id.temperature_min
                reading.temperature_max = reading.site_id.temperature_max
            else:
                reading.temperature_min = 0.0
                reading.temperature_max = 0.0

    @api.depends('temperature', 'temperature_min', 'temperature_max')
    def _compute_within_range(self):
        for reading in self:
            if reading.temperature < reading.temperature_min:
                reading.within_range = False
                reading.deviation = reading.temperature_min - reading.temperature
            elif reading.temperature > reading.temperature_max:
                reading.within_range = False
                reading.deviation = reading.temperature - reading.temperature_max
            else:
                reading.within_range = True
                reading.deviation = 0.0

    @api.depends('trip_id.name', 'site_id.name')
    def _compute_name(self):
        for reading in self:
            source = reading.trip_id.name or reading.site_id.name or 'Unknown'
            reading.name = '%s / %s' % (source, reading.reading_datetime)

    def _find_open_excursion(self):
        self.ensure_one()
        if self.trip_id:
            return self.env['sf.cold.excursion'].search([
                ('trip_id', '=', self.trip_id.id),
                ('state', '=', 'open'),
            ], limit=1)
        return self.env['sf.cold.excursion'].search([
            ('site_id', '=', self.site_id.id),
            ('state', '=', 'open'),
        ], limit=1)

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        excursion_model = self.env['sf.cold.excursion']
        for reading in records:
            if not reading.within_range:
                excursion = reading._find_open_excursion()
                if not excursion:
                    excursion = excursion_model.create({
                        'trip_id': reading.trip_id.id,
                        'site_id': reading.site_id.id,
                        'start_datetime': reading.reading_datetime,
                        'company_id': reading.company_id.id,
                    })
                reading.excursion_id = excursion.id
        return records