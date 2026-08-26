# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_staffing_mission_end_reminder_days = fields.Integer(
        string='Mission End Reminder (Days)',
        default=7,
        config_parameter='sf_staffing.mission_end_reminder_days',
    )