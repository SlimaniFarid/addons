# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_utility_anomaly_threshold = fields.Float(
        string='Abnormal Consumption Threshold',
        default=500.0,
        config_parameter='sf_utility_billing.anomaly_threshold',
    )
    sf_utility_default_revenue_account = fields.Many2one(
        'account.account',
        string='Default Revenue Account',
        config_parameter='sf_utility_billing.default_revenue_account',
    )