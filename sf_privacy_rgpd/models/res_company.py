# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_privacy_review_days = fields.Integer(
        string='Treatment review interval (days)', default=365)
    sf_privacy_breach_hours = fields.Integer(
        string='Breach notification deadline (hours)', default=72)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_privacy_review_days = fields.Integer(
        related='company_id.sf_privacy_review_days', readonly=False)
    sf_privacy_breach_hours = fields.Integer(
        related='company_id.sf_privacy_breach_hours', readonly=False)