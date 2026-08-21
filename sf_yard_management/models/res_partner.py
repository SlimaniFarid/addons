# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sf_yard_free_hours = fields.Float(
        string='Yard Free Time (h)', default=2.0,
        help='Free detention time granted to this carrier in your yards.')
    sf_yard_rate_per_hour = fields.Monetary(
        string='Yard Detention Rate/h', currency_field='currency_id',
        default=0.0,
        help='Detention charge per hour beyond the free time.')
