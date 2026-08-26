# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    sf_library_loan_days = fields.Integer(
        string='Loan duration days', default=21)
    sf_library_fine_per_day = fields.Float(
        string='Fine per day', default=0.50)
    sf_library_hold_days = fields.Integer(
        string='Reservation hold days', default=3)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sf_library_loan_days = fields.Integer(
        related='company_id.sf_library_loan_days', readonly=False)
    sf_library_fine_per_day = fields.Float(
        related='company_id.sf_library_fine_per_day', readonly=False)
    sf_library_hold_days = fields.Integer(
        related='company_id.sf_library_hold_days', readonly=False)
