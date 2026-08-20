# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_restaurant_avg_service_hours = fields.Float(
        string='Average Service Duration (Hours)',
        default=1.5,
        config_parameter='sf_restaurant.avg_service_hours',
    )
    sf_restaurant_services = fields.Integer(
        string='Number of Services',
        default=2,
        config_parameter='sf_restaurant.services',
    )