# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_dock_grace_minutes = fields.Integer(
        string='No-Show Grace (Minutes)',
        default=15,
        config_parameter='sf_dock_appointments.grace_minutes',
    )
    sf_dock_default_window_minutes = fields.Integer(
        string='Default Appointment Window (Minutes)',
        default=60,
        config_parameter='sf_dock_appointments.default_window_minutes',
    )