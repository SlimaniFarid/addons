# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_aql_default_inspection_level = fields.Selection([
        ('I', 'Level I'),
        ('II', 'Level II'),
        ('III', 'Level III'),
    ], string='Default Inspection Level',
        default='II',
        config_parameter='sf_aql_sampling.default_inspection_level',
    )
    sf_aql_enable_weighted_defects = fields.Boolean(
        string='Weight defects by severity',
        default=True,
        config_parameter='sf_aql_sampling.enable_weighted_defects',
    )