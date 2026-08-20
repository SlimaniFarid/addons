# -*- coding: utf-8 -*-
from odoo import fields, models


class SfParkingZone(models.Model):
    _name = 'sf.parking.zone'
    _description = 'Parking Zone'
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    site_id = fields.Many2one('sf.parking.site', string='Site', required=True, ondelete='cascade')
    capacity = fields.Integer(string='Capacity', default=0)
    place_ids = fields.One2many('sf.parking.place', 'zone_id', string='Places')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.parking.zone')
            if vals.get('site_id') and not vals.get('company_id'):
                site = self.env['sf.parking.site'].browse(vals['site_id'])
                vals['company_id'] = site.company_id.id
        return super().create(vals_list)