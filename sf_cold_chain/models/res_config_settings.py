# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_cold_chain_alert_hours = fields.Integer(
        string='Unresolved Excursion Alert After (Hours)',
        default=24,
        config_parameter='sf_cold_chain.alert_hours',
    )