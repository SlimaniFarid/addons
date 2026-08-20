# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_rework_alert_days = fields.Integer(
        string='Escalation Alert After (Days)',
        default=7,
        config_parameter='sf_rework_management.alert_days',
    )
    sf_rework_default_hourly_rate = fields.Float(
        string='Default Hourly Rate',
        default=0.0,
        config_parameter='sf_rework_management.default_hourly_rate',
    )