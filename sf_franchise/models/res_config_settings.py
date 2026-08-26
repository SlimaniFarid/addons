# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_franchise_default_royalty_account_id = fields.Many2one(
        'account.account',
        string='Default Royalty Income Account',
        config_parameter='sf_franchise.default_royalty_account_id',
    )
    sf_franchise_default_sale_journal_id = fields.Many2one(
        'account.journal',
        string='Default Sale Journal',
        config_parameter='sf_franchise.default_sale_journal_id',
    )