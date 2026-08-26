# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_warranty_auto_check = fields.Boolean(
        string='Check eligibility when opening a claim', default=True)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_warranty_auto_check = fields.Boolean(
        related='company_id.sf_warranty_auto_check', readonly=False)