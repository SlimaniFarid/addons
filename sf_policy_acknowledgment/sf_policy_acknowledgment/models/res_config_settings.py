# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_policy_expiry_reminder_days = fields.Integer(
        string='Expiry Reminder (days before expiry)',
        default=30,
        config_parameter='sf_policy_acknowledgment.expiry_reminder_days',
    )