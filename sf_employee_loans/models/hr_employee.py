# -*- coding: utf-8 -*-
from odoo import fields, models


class EmployeeLoanHrEmployee(models.Model):
    _inherit = 'hr.employee'

    sf_loan_ids = fields.One2many('sf.employee.loan', 'employee_id',
                                  string='Loans')