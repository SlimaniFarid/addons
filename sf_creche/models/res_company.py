# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_creche_alert_days = fields.Integer(
        string='Enrollment end alert (days)', default=14)
    sf_creche_hourly_rate = fields.Float(
        string='Hourly billing rate', default=4.0)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_creche_alert_days = fields.Integer(
        related='company_id.sf_creche_alert_days', readonly=False)
    sf_creche_hourly_rate = fields.Float(
        related='company_id.sf_creche_hourly_rate', readonly=False)
