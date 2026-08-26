# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_events_reminder_days = fields.Integer(
        string='Reminder Days Before Event',
        default=7,
        config_parameter='sf_events.reminder_days',
    )