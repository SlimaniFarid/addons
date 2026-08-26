# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_pim_score_threshold = fields.Float(
        string='PIM minimum completeness (%)', default=100.0)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_pim_score_threshold = fields.Float(
        related='company_id.sf_pim_score_threshold', readonly=False)