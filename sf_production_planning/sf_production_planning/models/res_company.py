# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_mps_load_draft_only = fields.Boolean(
        string='Load only draft manufacturing orders', default=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_mps_load_draft_only = fields.Boolean(
        related='company_id.sf_mps_load_draft_only', readonly=False)