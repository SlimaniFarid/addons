# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_hotel_alert_days = fields.Integer(
        string='Departure alert (days)', default=1)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_hotel_alert_days = fields.Integer(
        related='company_id.sf_hotel_alert_days', readonly=False)
