# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_fuel_alert_days = fields.Integer(
        string='Fuel card expiry alert (days)', default=7)
    sf_fuel_max_l100 = fields.Float(
        string='Max consumption alert (L/100km)', default=12.0)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_fuel_alert_days = fields.Integer(
        related='company_id.sf_fuel_alert_days', readonly=False)
    sf_fuel_max_l100 = fields.Float(
        related='company_id.sf_fuel_max_l100', readonly=False)