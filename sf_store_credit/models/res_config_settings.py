# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_store_credit_expiry_reminder_days = fields.Integer(
        string='Expiry Reminder Delay (days)',
        default=7,
        config_parameter='sf_store_credit.expiry_reminder_days',
    )