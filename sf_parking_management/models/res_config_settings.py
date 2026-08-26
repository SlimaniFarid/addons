# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_parking_default_hourly_rate = fields.Monetary(
        string='Default Hourly Rate',
        default=2.0,
        config_parameter='sf_parking_management.default_hourly_rate',
    )
    sf_parking_default_daily_rate = fields.Monetary(
        string='Default Daily Rate',
        default=12.0,
        config_parameter='sf_parking_management.default_daily_rate',
    )
    sf_parking_revenue_account_id = fields.Many2one(
        'account.account',
        string='Revenue Account',
        config_parameter='sf_parking_management.revenue_account_id',
    )