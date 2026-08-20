# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_invest_alert_days = fields.Integer(
        string='Maturity alert margin (days)', default=15)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_invest_alert_days = fields.Integer(
        related='company_id.sf_invest_alert_days', readonly=False)