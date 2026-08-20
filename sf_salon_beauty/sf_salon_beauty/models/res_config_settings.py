# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_salon_default_commission_rate = fields.Float(
        string='Default Commission Rate (%)',
        default=10.0,
        config_parameter='sf_salon_beauty.default_commission_rate',
    )
    sf_salon_default_duration = fields.Integer(
        string='Default Service Duration (Minutes)',
        default=30,
        config_parameter='sf_salon_beauty.default_duration',
    )