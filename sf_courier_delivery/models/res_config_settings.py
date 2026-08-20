# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_courier_default_price = fields.Float(
        string='Default Delivery Price',
        default=5.0,
        config_parameter='sf_courier_delivery.default_price',
    )
    sf_courier_revenue_account_id = fields.Many2one(
        'account.account',
        string='Revenue Account',
        config_parameter='sf_courier_delivery.revenue_account_id',
    )