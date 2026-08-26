# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_grant_alert_days = fields.Integer(
        string='Grant deadline alert margin (days)', default=7)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_grant_alert_days = fields.Integer(
        related='company_id.sf_grant_alert_days', readonly=False)