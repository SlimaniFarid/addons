# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_laundry_expected_delivery_days = fields.Integer(
        string='Default Delivery Delay (Days)',
        default=3,
        config_parameter='sf_laundry.expected_delivery_days',
    )
    sf_laundry_slow_threshold_hours = fields.Integer(
        string='Slow Treatment Threshold (Hours)',
        default=72,
        config_parameter='sf_laundry.slow_threshold_hours',
    )