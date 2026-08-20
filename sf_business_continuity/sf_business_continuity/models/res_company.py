# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_bcp_review_days = fields.Integer(
        string='BCP plan review interval (days)', default=365)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_bcp_review_days = fields.Integer(
        related='company_id.sf_bcp_review_days', readonly=False)