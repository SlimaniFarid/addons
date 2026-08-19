# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_loan_alert_days = fields.Integer(
        string='Loan alert delay (days)', default=15)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_loan_alert_days = fields.Integer(
        related='company_id.sf_loan_alert_days', readonly=False)