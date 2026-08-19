# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EmployeeLoanLine(models.Model):
    _name = 'sf.employee.loan.line'
    _description = 'Employee Loan Repayment Line'
    _order = 'due_date, sequence'

    loan_id = fields.Many2one('sf.employee.loan', string='Loan',
                              required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence')
    due_date = fields.Date(string='Due Date', required=True)
    amount = fields.Monetary(string='Amount',
                             currency_field='currency_id')
    currency_id = fields.Many2one(related='loan_id.currency_id',
                                  string='Currency')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('missed', 'Missed'),
        ('written_off', 'Written Off'),
    ], string='Status', default='pending', tracking=True)
    paid_date = fields.Date(string='Paid Date')
    notes = fields.Text(string='Notes')

    def _apply_last_line_adjustment(self):
        loan = self.loan_id
        paid = sum(line.amount for line in loan.lines
                   if line.id != self.id)
        self.amount = round(loan.total_amount - paid, 2)

    def action_record_payment(self):
        today = fields.Date.today()
        for line in self:
            if line.state != 'pending':
                raise UserError(_('Only pending lines can be paid.'))
            line.state = 'paid'
            line.paid_date = today
            line.loan_id.message_post(body=_(
                'Repayment of %s recorded.') % line.amount)

    def action_mark_missed(self):
        for line in self:
            if line.state != 'pending':
                raise UserError(
                    _('Only pending lines can be marked as missed.'))
            line.state = 'missed'

    def action_write_off(self):
        for line in self:
            if line.state != 'missed':
                raise UserError(
                    _('Only missed lines can be written off.'))
            line.state = 'written_off'

    def action_pay_all(self):
        for line in self:
            if line.state == 'pending':
                line.action_record_payment()