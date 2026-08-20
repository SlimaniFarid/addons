# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Property(models.Model):
    _name = 'sf.realestate.property'
    _description = 'Property'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, size=20)
    property_type = fields.Selection([
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('office', 'Office'),
        ('retail', 'Retail'),
        ('land', 'Land'),
        ('warehouse', 'Warehouse'),
    ], string='Type', default='apartment', required=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
        ('sold', 'Sold'),
    ], string='Status', default='available', tracking=True)
    owner_id = fields.Many2one('res.partner', string='Owner')
    address = fields.Char(string='Address')
    city = fields.Char(string='City')
    zip = fields.Char(string='ZIP')
    country_id = fields.Many2one('res.country', string='Country')
    surface = fields.Float(string='Surface (m2)')
    value = fields.Monetary(string='Market Value')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    lease_ids = fields.One2many('sf.realestate.lease', 'property_id',
                                string='Leases')
    current_lease_id = fields.Many2one(
        'sf.realestate.lease', string='Current Lease',
        compute='_compute_current_lease')
    monthly_rent = fields.Monetary(
        string='Monthly Rent', compute='_compute_current_lease')
    occupancy = fields.Float(
        string='Occupancy (%)', compute='_compute_current_lease')

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Property code must be unique.'),
    ]

    @api.depends('lease_ids', 'lease_ids.state', 'lease_ids.rent')
    def _compute_current_lease(self):
        today = fields.Date.context_today(self)
        for prop in self:
            current = prop.lease_ids.filtered(
                lambda l: l.state == 'active'
                and l.date_start <= today
                and (not l.date_end or l.date_end >= today))
            prop.current_lease_id = current[:1]
            prop.monthly_rent = current[:1].rent or 0.0
            prop.occupancy = 100.0 if current else 0.0

    def action_available(self):
        self.write({'state': 'available'})

    def action_maintenance(self):
        self.write({'state': 'maintenance'})