# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_waste_alert_days = fields.Integer(
        string='Waste reception alert (days)',
        default=15)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_waste_alert_days = fields.Integer(
        related='company_id.sf_waste_alert_days', readonly=False)