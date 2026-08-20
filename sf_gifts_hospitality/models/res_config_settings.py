# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_gifts_hospitality_approval_threshold = fields.Monetary(
        string='Approval Threshold',
        default=50.0,
        config_parameter='sf_gifts_hospitality.approval_threshold',
    )