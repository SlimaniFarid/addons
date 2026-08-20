# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_batch_records_block_out_of_spec_release = fields.Boolean(
        string='Block release on out-of-spec parameters',
        default=True,
        config_parameter='sf_batch_records.block_out_of_spec_release',
    )