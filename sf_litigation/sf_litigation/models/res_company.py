# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_litigation_alert_days = fields.Integer(
        string='Deadline alert (days)', default=10)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_litigation_alert_days = fields.Integer(
        related='company_id.sf_litigation_alert_days', readonly=False)