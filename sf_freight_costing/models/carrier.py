# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class FreightCarrier(models.Model):
    _name = 'sf.freight.carrier'
    _description = 'Freight Carrier'
    _rec_name = 'name'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    partner_id = fields.Many2one('res.partner', string='Carrier Partner')
    cost_method = fields.Selection([
        ('fixed', 'Fixed Price'),
        ('weight', 'Per Kilogram'),
        ('volume', 'Per Cubic Meter'),
        ('value', 'Percentage of Value'),
    ], string='Cost Method', default='fixed', required=True)
    fixed_price = fields.Float(string='Fixed Price', default=0.0)
    per_kg = fields.Float(string='Price per KG', default=0.0)
    per_m3 = fields.Float(string='Price per m3', default=0.0)
    percent_value = fields.Float(string='% of Value', default=0.0)
    min_charge = fields.Float(string='Minimum Charge', default=0.0)
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  default=lambda self: self.env.company.currency_id)
    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('code_uniq', 'unique(code)', 'Carrier code must be unique.'),
    ]

    @api.model
    def compute_cost(self, carrier, weight, volume, value):
        """Compute freight cost for given weight/volume/value."""
        if carrier.cost_method == 'fixed':
            return max(carrier.fixed_price, carrier.min_charge)
        if carrier.cost_method == 'weight':
            return max(weight * carrier.per_kg, carrier.min_charge)
        if carrier.cost_method == 'volume':
            return max(volume * carrier.per_m3, carrier.min_charge)
        if carrier.cost_method == 'value':
            return max(value * carrier.percent_value / 100.0,
                       carrier.min_charge)
        return 0.0