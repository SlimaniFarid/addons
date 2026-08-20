# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_digital_delivery_default_key_format = fields.Char(
        string='Default License Key Format',
        default='XXXX-XXXX-XXXX',
        config_parameter='sf_digital_delivery.default_key_format',
    )
    sf_digital_delivery_default_validity_days = fields.Integer(
        string='Default Download Link Validity (days)',
        default=30,
        config_parameter='sf_digital_delivery.default_validity_days',
    )
    sf_digital_delivery_default_activation_days = fields.Integer(
        string='Default Key Activation Delay (days)',
        default=30,
        config_parameter='sf_digital_delivery.default_activation_days',
    )