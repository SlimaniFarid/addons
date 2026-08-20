# -*- coding: utf-8 -*-
from odoo import fields, models, _


class AndonStation(models.Model):
    _name = 'sf.andon.station'
    _description = 'Andon Station'
    _rec_name = 'name'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    line_id = fields.Many2one('mrp.workcenter', string='Production Line / Workcenter')
    location = fields.Char(string='Physical Location')
    tower_light_ip = fields.Char(string='Tower Light IP Address')
    tower_light_port = fields.Integer(string='Tower Light Port', default=502)
    screen_url = fields.Char(string='Display Screen URL')
    active = fields.Boolean(string='Active', default=True)
    call_ids = fields.One2many('sf.andon.call', 'station_id', string='Andon Calls')
    open_calls_count = fields.Integer(string='Open Calls', compute='_compute_counts')
    active_operators = fields.Many2many('res.users', string='Active Operators')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Station code must be unique.'),
    ]

    def _compute_counts(self):
        for station in self:
            station.open_calls_count = len(station.call_ids.filtered(
                lambda c: c.state in ('new', 'acknowledged', 'in_progress')))