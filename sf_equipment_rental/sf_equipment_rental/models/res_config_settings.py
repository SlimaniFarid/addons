# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_rental_penalty_account_id = fields.Many2one(
        'account.account',
        string='Penalty Account',
        config_parameter='sf_equipment_rental.penalty_account_id',
    )