# -*- coding: utf-8 -*-
from odoo import api, fields, models


class EnergyMeter(models.Model):
    _name = 'sf.energy.meter'
    _description = 'Energy Meter'
    _order = 'site_id, name'

    name = fields.Char(string='Name', required=True)
    site_id = fields.Many2one('sf.energy.site', string='Site',
                              required=True, ondelete='cascade')
    utility_type = fields.Selection([
        ('electricity', 'Electricity'),
        ('gas', 'Gas'),
        ('water', 'Water'),
    ], string='Utility', required=True)
    unit = fields.Selection([
        ('kwh', 'kWh'),
        ('m3', 'm³'),
    ], string='Unit', compute='_compute_unit', store=True)
    price_unit = fields.Float(string='Unit Price',
                              help='Price per unit in company currency')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    state = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string='Status', default='active')
    reading_ids = fields.One2many('sf.energy.reading', 'meter_id',
                                  string='Readings')
    last_reading_date = fields.Date(string='Last Reading',
                                    compute='_compute_last_reading',
                                    store=True)
    last_index = fields.Float(string='Last Index',
                              compute='_compute_last_reading', store=True)

    @api.depends('utility_type')
    def _compute_unit(self):
        for meter in self:
            meter.unit = 'kwh' if meter.utility_type == 'electricity' \
                else 'm3'

    @api.depends('reading_ids.state', 'reading_ids.date',
                 'reading_ids.index_value')
    def _compute_last_reading(self):
        for meter in self:
            readings = meter.reading_ids.filtered(
                lambda r: r.state == 'confirmed')
            last = readings.sorted(key=lambda r: r.date, reverse=True)
            meter.last_reading_date = last[0].date if last else False
            meter.last_index = last[0].index_value if last else 0.0

    def action_activate(self):
        self.state = 'active'

    def action_deactivate(self):
        self.state = 'inactive'