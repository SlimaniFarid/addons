# -*- coding: utf-8 -*-
from odoo import _, fields, models
from odoo.exceptions import UserError


class SfRentalEquipment(models.Model):
    _name = 'sf.rental.equipment'
    _description = 'Rental Equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'sf.rental.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Name', required=True, copy=False)
    category_id = fields.Many2one('sf.rental.category', string='Category', ondelete='restrict')
    serial = fields.Char(string='Serial Number')
    purchase_value = fields.Monetary(string='Purchase Value', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id', readonly=True, store=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('out', 'Out'),
        ('maintenance', 'Maintenance'),
        ('retired', 'Retired'),
    ], string='Status', default='available')
    hourly_price = fields.Monetary(string='Hourly Price', currency_field='currency_id')
    daily_price = fields.Monetary(string='Daily Price', currency_field='currency_id')
    weekly_price = fields.Monetary(string='Weekly Price', currency_field='currency_id')
    monthly_price = fields.Monetary(string='Monthly Price', currency_field='currency_id')
    company_id = fields.Many2one('res.company', string='Company', store=True, default=lambda self: self.env.company)

    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('name'):
                vals['name'] = self.env['ir.sequence'].next_by_code('sf.rental.equipment')
            if vals.get('state', 'available') != 'available':
                raise UserError(_('Equipment can only be created as available.'))
        return super().create(vals_list)