# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_correspondence_default_reminder_days = fields.Integer(
        string='Response Reminder (days before due)',
        default=2,
        config_parameter='sf_correspondence.default_reminder_days',
    )