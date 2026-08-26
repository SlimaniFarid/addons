# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_workshop_alert_days = fields.Integer(
        string='Unassigned request alert (days)', default=7)
    sf_workshop_hourly_rate = fields.Float(
        string='Workshop hourly rate', default=50.0)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_workshop_alert_days = fields.Integer(
        related='company_id.sf_workshop_alert_days', readonly=False)
    sf_workshop_hourly_rate = fields.Float(
        related='company_id.sf_workshop_hourly_rate', readonly=False)