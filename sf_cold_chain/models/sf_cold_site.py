# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SfColdSite(models.Model):
    _name = 'sf.cold.site'
    _description = 'Cold Storage Site'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.cold.chain.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    location = fields.Char(string='Location')
    device_type = fields.Selection([
        ('cold_room', 'Cold Room'),
        ('fridge', 'Fridge'),
        ('freezer', 'Freezer'),
    ], string='Device Type', required=True, default='cold_room')
    target_min_temp = fields.Float(string='Target Min Temp', required=True,
                                   default=2.0)
    target_max_temp = fields.Float(string='Target Max Temp', required=True,
                                   default=8.0)
    state = fields.Selection([
        ('monitored', 'Monitored'),
        ('out_of_range', 'Out of Range'),
    ], string='Status', compute='_compute_state', store=True)
    reading_ids = fields.One2many('sf.cold.reading', 'site_id', string='Readings')
    excursion_ids = fields.One2many('sf.cold.excursion', 'site_id', string='Excursions')
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.constrains('target_min_temp', 'target_max_temp')
    def _check_temperature_range(self):
        for site in self:
            if site.target_max_temp < site.target_min_temp:
                raise ValidationError(_(
                    'The maximum temperature cannot be lower than the minimum temperature.'))

    @api.depends('reading_ids.within_range')
    def _compute_state(self):
        for site in self:
            out_of_range = site.reading_ids.filtered(lambda r: not r.within_range)
            site.state = 'out_of_range' if out_of_range else 'monitored'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.cold.site')
        return super().create(vals_list)