# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_haccp_alert_days = fields.Integer(
        string='HACCP control reminder (days)', default=0)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_haccp_alert_days = fields.Integer(
        related='company_id.sf_haccp_alert_days', readonly=False)