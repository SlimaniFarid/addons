# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_medical_alert_days = fields.Integer(string='Appointment alert (days)',
                                           default=2)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_medical_alert_days = fields.Integer(
        related='company_id.sf_medical_alert_days', readonly=False)