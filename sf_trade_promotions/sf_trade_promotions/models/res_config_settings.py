# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_trade_promotions_validation_threshold = fields.Float(
        string='Validation Threshold',
        default=0.0,
        config_parameter='sf_trade_promotions.validation_threshold',
    )
    sf_trade_promotions_product_account_id = fields.Many2one(
        'account.account',
        string='Product Account (future invoicing)',
        config_parameter='sf_trade_promotions.product_account_id',
    )