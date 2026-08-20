# -*- coding: utf-8 -*-
from odoo import fields, models


class SfRestaurantZone(models.Model):
    _name = 'sf.restaurant.zone'
    _description = 'Restaurant Zone'
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    table_ids = fields.One2many('sf.restaurant.table', 'zone_id', string='Tables')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.restaurant.zone')
        return super().create(vals_list)