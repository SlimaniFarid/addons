# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_business_travel_reminder_days = fields.Integer(
        string='Departure Reminder (days before departure)',
        default=2,
        config_parameter='sf_business_travel.reminder_days',
    )