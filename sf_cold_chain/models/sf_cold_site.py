# -*- coding: utf-8 -*-
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SfColdSite(models.Model):
    _name = 'sf.cold.site'
    _description = 'Cold Storage Site'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.cold.chain.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    site_type = fields.Selection([
        ('cold_storage', 'Cold Storage'),
        ('refrigerated_transport', 'Refrigerated Transport'),
        ('chamber', 'Chamber'),
        ('freezer', 'Freezer'),
        ('cold_room', 'Cold Room'),
    ], string='Site Type', required=True, default='cold_storage')
    temperature_min = fields.Float(string='Min Temperature', required=True,
                                   default=2.0)
    temperature_max = fields.Float(string='Max Temperature', required=True,
                                   default=8.0)
    location_note = fields.Char(string='Location')
    is_active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company', store=True,
                                 default=lambda self: self.env.company)

    @api.constrains('temperature_min', 'temperature_max')
    def _check_temperature_range(self):
        for site in self:
            if site.temperature_max < site.temperature_min:
                raise ValidationError(_(
                    'The maximum temperature cannot be lower than the minimum temperature.'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.cold.site')
        return super().create(vals_list)