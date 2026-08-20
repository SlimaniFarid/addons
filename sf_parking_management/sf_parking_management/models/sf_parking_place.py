# -*- coding: utf-8 -*-
from odoo import fields, models


class SfParkingPlace(models.Model):
    _name = 'sf.parking.place'
    _description = 'Parking Place'
    _order = 'number asc'

    name = fields.Char(string='Name', required=True, copy=False)
    zone_id = fields.Many2one('sf.parking.zone', string='Zone', required=True, ondelete='cascade')
    number = fields.Char(string='Number')
    state = fields.Selection([
        ('free', 'Free'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('out_of_service', 'Out of Service'),
    ], string='Status', default='free')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.parking.place')
            if vals.get('zone_id') and not vals.get('company_id'):
                zone = self.env['sf.parking.zone'].browse(vals['zone_id'])
                vals['company_id'] = zone.company_id.id
        return super().create(vals_list)