# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_tender_alert_days = fields.Integer(
        string='Tender deadline alert (days)', default=3)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_tender_alert_days = fields.Integer(
        related='company_id.sf_tender_alert_days', readonly=False)