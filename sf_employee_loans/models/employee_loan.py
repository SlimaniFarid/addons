# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class EmployeeLoan(models.Model):
    _name = 'sf.employee.loan'
    _description = 'Employee Loan'
    _inherit = ['mail.thread']
    _rec_name = 'employee_id'
    _order = 'start_date desc'

    employee_id = fields.Many2one('hr.employee', string='Employee',
                                  required=True)
    partner_id = fields.Many2one('res.partner', string='Payroll Partner',
                                 compute='_compute_partner_id', store=True)
    loan_type = fields.Selection([
        ('advance', 'Advance'),
        ('loan', 'Loan'),
    ], string='Loan Type', default='loan', required=True,
       tracking=True)
    amount = fields.Monetary(string='Loan Amount', required=True,
                             currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency',
                                  required=True,
                                  default=lambda self: self.env.company.currency_id)
    interest_rate = fields.Float(string='Annual Interest Rate (%)',
                                 default=0.0)
    duration_months = fields.Integer(string='Duration (months)',
                                     default=12, required=True)
    total_interest = fields.Monetary(string='Total Interest',
                                     compute='_compute_schedule', store=True,
                                     currency_field='currency_id')
    total_amount = fields.Monetary(string='Total Repayable',
                                   compute='_compute_schedule', store=True,
                                   currency_field='currency_id')
    monthly_amount = fields.Monetary(string='Monthly Instalment',
                                     compute='_compute_schedule', store=True,
                                     currency_field='currency_id')
    start_date = fields.Date(string='Start Date')
    lines = fields.One2many('sf.employee.loan.line', 'loan_id',
                            string='Repayment Lines')
    balance_due = fields.Monetary(string='Balance Due',
                                  compute='_compute_balance', store=True,
                                  currency_field='currency_id')
    paid_amount = fields.Monetary(string='Paid Amount',
                                  compute='_compute_balance', store=True,
                                  currency_field='currency_id')
    overdue_lines = fields.Integer(string='Overdue Lines',
                                   compute='_compute_balance', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    approved_by = fields.Many2one('res.users', string='Approved By')
    approval_date = fields.Datetime(string='Approval Date')
    company_id = fields.Many2one('res.company', string='Company',
                                 required=True,
                                 default=lambda self: self.env.company)
    notes = fields.Text(string='Notes')

    @api.depends('employee_id')
    def _compute_partner_id(self):
        for loan in self:
            loan.partner_id = loan.employee_id.work_contact_id

    @api.depends('amount', 'interest_rate', 'duration_months')
    def _compute_schedule(self):
        for loan in self:
            interest = loan.amount * (loan.interest_rate / 100.0) * (
                loan.duration_months / 12.0)
            loan.total_interest = round(interest, 2)
            loan.total_amount = round(loan.amount + interest, 2)
            if loan.duration_months:
                loan.monthly_amount = round(
                    loan.total_amount / loan.duration_months, 2)

    @api.depends('lines.state', 'lines.amount')
    def _compute_balance(self):
        for loan in self:
            paid = sum(line.amount for line in loan.lines
                       if line.state == 'paid')
            loan.paid_amount = paid
            loan.balance_due = loan.total_amount - paid
            loan.overdue_lines = sum(
                1 for line in loan.lines
                if line.state == 'pending'
                and line.due_date
                and line.due_date < fields.Date.today())

    @api.constrains('amount', 'interest_rate', 'duration_months')
    def _check_values(self):
        for loan in self:
            if loan.amount <= 0:
                raise UserError(_('The loan amount must be positive.'))
            if not 1 <= loan.duration_months <= 120:
                raise UserError(
                    _('The loan duration must be between 1 and 120 months.'))
            if loan.interest_rate < 0:
                raise UserError(
                    _('The interest rate cannot be negative.'))

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.company_id = self.employee_id.company_id or self.env.company
            self.partner_id = self.employee_id.work_contact_id

    def _check_ceiling(self):
        self.ensure_one()
        ceiling = self.company_id.sf_max_advance
        if not ceiling:
            return
        existing = sum(
            loan.balance_due for loan in self.env['sf.employee.loan'].search([
                ('employee_id', '=', self.employee_id.id),
                ('state', 'in', ('submitted', 'approved', 'active')),
                ('id', '!=', self.id),
            ]))
        if existing + self.amount > ceiling:
            raise UserError(
                _('This request exceeds the advance ceiling of %s for '
                  'the company.') % ceiling)

    def action_submit(self):
        for loan in self:
            if loan.state != 'draft':
                raise UserError(_('Only draft loans can be submitted.'))
            loan._check_ceiling()
            loan.state = 'submitted'
            loan.message_post(body=_('Loan request submitted for approval.'))

    def action_approve(self):
        if not self.env.user.has_group(
                'sf_employee_loans.group_employee_loans_manager'):
            raise UserError(_('Only managers can approve loan requests.'))
        for loan in self:
            if loan.state != 'submitted':
                raise UserError(
                    _('Only submitted loans can be approved.'))
            loan._check_ceiling()
            loan.state = 'approved'
            loan.approved_by = self.env.user
            loan.approval_date = fields.Datetime.now()
            loan.message_post(body=_('Loan request approved.'))

    def action_reject(self):
        for loan in self:
            if loan.state != 'submitted':
                raise UserError(
                    _('Only submitted loans can be rejected.'))
            loan.state = 'rejected'
            loan.message_post(body=_('Loan request rejected.'))

    def action_cancel(self):
        for loan in self:
            if loan.state not in ('submitted', 'approved'):
                raise UserError(
                    _('Only submitted or approved loans can be cancelled.'))
            loan.state = 'cancelled'
            loan.message_post(body=_('Loan request cancelled.'))

    def action_validate(self):
        for loan in self:
            if loan.state != 'approved':
                raise UserError(
                    _('Only approved loans can be activated.'))
            loan._check_ceiling()
            loan.start_date = loan.start_date or fields.Date.today()
            loan._generate_schedule()
            loan.state = 'active'
            loan.message_post(body=_('Loan activated and repayment '
                                     'schedule generated.'))

    def _generate_schedule(self):
        self.ensure_one()
        self.lines.unlink()
        vals_list = []
        for month in range(1, self.duration_months + 1):
            due_date = self._get_due_date(self.start_date, month)
            vals_list.append({
                'loan_id': self.id,
                'sequence': month,
                'due_date': due_date,
                'amount': self.monthly_amount,
            })
        if vals_list:
            lines = self.env['sf.employee.loan.line'].create(vals_list)
            lines[-1]._apply_last_line_adjustment()

    def _get_due_date(self, start_date, month):
        base = fields.Date.from_string(start_date)
        year = base.year + (base.month - 1 + month) // 12
        month_num = (base.month - 1 + month) % 12 + 1
        day = min(base.day, 28)
        from datetime import date
        return date(year, month_num, day)

    def action_close(self):
        for loan in self:
            if loan.state != 'active':
                raise UserError(_('Only active loans can be closed.'))
            if any(line.state != 'paid' for line in loan.lines):
                raise UserError(
                    _('All repayment lines must be paid before closing.'))
            loan.state = 'closed'
            loan.message_post(body=_('Loan closed.'))

    def unlink(self):
        for loan in self:
            if loan.state in ('active', 'closed'):
                raise UserError(
                    _('An active or closed loan cannot be deleted.'))
        return super().unlink()