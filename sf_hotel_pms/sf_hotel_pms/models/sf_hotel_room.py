# -*- coding: utf-8 -*-
from odoo import api, fields, models


class SfHotelRoom(models.Model):
    _name = 'sf.hotel.room'
    _description = 'Hotel Room'
    _order = 'number'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Number', required=True, index=True)
    number = fields.Integer(string='Room number', index=True)
    floor = fields.Char(string='Floor')
    room_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('twin', 'Twin'),
        ('suite', 'Suite'),
        ('other', 'Other'),
    ], string='Room type', required=True, default='single')
    capacity = fields.Integer(string='Capacity', default=1)
    base_price = fields.Float(string='Base price per night')
    status = fields.Selection([
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
        ('reserved', 'Reserved'),
    ], string='Status', default='available', required=True, tracking=True,
       index=True)
    housekeeping_ids = fields.One2many('sf.hotel.housekeeping', 'room_id',
                                       string='Housekeeping tasks')
    active = fields.Boolean(string='Active', default=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sf.hotel.room')
        return super().create(vals)
