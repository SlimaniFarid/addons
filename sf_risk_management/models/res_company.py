# -*- coding: utf-8 -*-
from odoo import fields, models


class RiskResCompany(models.Model):
    _inherit = 'res.company'

    sf_risk_high_threshold = fields.Integer(
        string='High Risk Threshold', default=9)
    sf_risk_extreme_threshold = fields.Integer(
        string='Extreme Risk Threshold', default=17)