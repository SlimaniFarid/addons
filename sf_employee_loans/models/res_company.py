# -*- coding: utf-8 -*-
from odoo import fields, models


class EmployeeLoanResCompany(models.Model):
    _inherit = 'res.company'

    sf_max_advance = fields.Monetary(string='Max Advance per Employee',
                                     currency_field='currency_id')