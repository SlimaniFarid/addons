# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_compliance_alert_days = fields.Integer(
        string='Certificate expiry alert (days)', default=30)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_compliance_alert_days = fields.Integer(
        related='company_id.sf_compliance_alert_days', readonly=False)