# -*- coding: utf-8 -*-
from odoo import fields, models


class SfRestaurantTable(models.Model):
    _name = 'sf.restaurant.table'
    _description = 'Restaurant Table'
    _order = 'name'

    name = fields.Char(string='Name', required=True, copy=False)
    zone_id = fields.Many2one('sf.restaurant.zone', string='Zone', ondelete='set null')
    seats = fields.Integer(string='Seats', default=2)
    state = fields.Selection([
        ('free', 'Free'),
        ('reserved', 'Reserved'),
        ('occupied', 'Occupied'),
        ('cleaning', 'Cleaning'),
    ], string='Status', default='free', copy=False)
    current_order_id = fields.Many2one('sf.restaurant.order', string='Current Order', ondelete='set null', readonly=True)
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.restaurant.table')
        return super().create(vals_list)