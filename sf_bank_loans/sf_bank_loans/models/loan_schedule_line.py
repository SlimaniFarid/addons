# -*- coding: utf-8 -*-
from odoo import fields, models


class SfLoanScheduleLine(models.Model):
    _name = 'sf.loan.schedule.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Loan Schedule Line'
    _order = 'loan_id, line_number'

    loan_id = fields.Many2one('sf.loan', string='Loan', required=True,
                              ondelete='cascade', index=True)
    line_number = fields.Integer(string='Line', required=True)
    due_date = fields.Date(string='Due date')
    principal = fields.Float(string='Principal')
    interest = fields.Float(string='Interest')
    total = fields.Float(string='Total')
    paid = fields.Boolean(string='Paid', default=False)
    paid_date = fields.Date(string='Paid date')
    company_id = fields.Many2one('res.company', string='Company',
                                 related='loan_id.company_id', store=True,
                                 readonly=True)