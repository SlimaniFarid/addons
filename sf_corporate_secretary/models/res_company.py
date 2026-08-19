# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_corporate_default_notice_days = fields.Integer(
        string='Default notice period (days)', default=15)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_corporate_default_notice_days = fields.Integer(
        related='company_id.sf_corporate_default_notice_days',
        readonly=False)