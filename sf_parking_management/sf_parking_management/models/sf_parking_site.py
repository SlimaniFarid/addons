# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SfParkingSite(models.Model):
    _name = 'sf.parking.site'
    _description = 'Parking Site'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.parking.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    address = fields.Text(string='Address')
    capacity = fields.Integer(string='Capacity', required=True, default=1)
    hourly_rate = fields.Monetary(string='Hourly Rate', currency_field='currency_id')
    daily_rate = fields.Monetary(string='Daily Rate', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    zone_ids = fields.One2many('sf.parking.zone', 'site_id', string='Zones')
    ticket_ids = fields.One2many('sf.parking.ticket', 'site_id', string='Tickets')
    open_tickets = fields.Integer(string='Open Tickets', compute='_compute_open_tickets', store=True)
    occupancy_rate = fields.Float(string='Occupancy Rate (%)', compute='_compute_occupancy_rate', store=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    @api.depends('ticket_ids.state')
    def _compute_open_tickets(self):
        for site in self:
            site.open_tickets = len(site.ticket_ids.filtered(lambda t: t.state == 'open'))

    @api.depends('open_tickets', 'capacity')
    def _compute_occupancy_rate(self):
        for site in self:
            site.occupancy_rate = site.capacity and round(site.open_tickets * 100.0 / site.capacity, 1) or 0.0

    def _check_manager(self):
        if not self.env.user.has_group('sf_parking_management.group_sf_parking_manager'):
            raise UserError(_('Only a parking manager can modify the rates.'))

    def _default_rates(self):
        param = self.env['ir.config_parameter'].sudo()
        settings = self.env['res.config.settings']
        hourly_param = param.get_param('sf_parking_management.default_hourly_rate')
        hourly = float(hourly_param) if hourly_param else \
            settings._fields['sf_parking_default_hourly_rate'].default or 0.0
        daily_param = param.get_param('sf_parking_management.default_daily_rate')
        daily = float(daily_param) if daily_param else \
            settings._fields['sf_parking_default_daily_rate'].default or 0.0
        return hourly, daily

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.parking.site')
            if 'hourly_rate' not in vals or 'daily_rate' not in vals:
                hourly, daily = self._default_rates()
                if 'hourly_rate' not in vals:
                    vals['hourly_rate'] = hourly
                if 'daily_rate' not in vals:
                    vals['daily_rate'] = daily
        return super().create(vals_list)

    def write(self, vals):
        if 'hourly_rate' in vals or 'daily_rate' in vals:
            self._check_manager()
        return super().write(vals)