# -*- coding: utf-8 -*-
from odoo import fields, models


class EnergySite(models.Model):
    _name = 'sf.energy.site'
    _description = 'Energy Site'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    address = fields.Text(string='Address')
    meter_ids = fields.One2many('sf.energy.meter', 'site_id',
                                string='Meters')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')