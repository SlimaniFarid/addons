# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_insurance_remind_days = fields.Integer(
        string='Renewal reminder (days)', default=30)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_insurance_remind_days = fields.Integer(
        related='company_id.sf_insurance_remind_days', readonly=False)
