# -*- coding: utf-8 -*-
import calendar
from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class SfLoan(models.Model):
    _name = 'sf.loan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Bank Loan'
    _order = 'start_date desc, id desc'

    name = fields.Char(string='Number', required=True, index=True)
    bank_id = fields.Many2one('sf.loan.bank', string='Bank',
                              required=True, ondelete='restrict', index=True)
    loan_type = fields.Selection([
        ('investment', 'Investment'),
        ('cashflow', 'Cash Flow'),
        ('overdraft', 'Overdraft'),
        ('other', 'Other'),
    ], string='Loan type', default='investment', required=True)
    amount = fields.Float(string='Amount', required=True)
    rate = fields.Float(string='Rate (%)', required=True)
    term_months = fields.Integer(string='Term (months)', required=True)
    amortization = fields.Selection([
        ('constant', 'Constant'),
        ('annuity', 'Annuity'),
    ], string='Amortization', default='annuity', required=True)
    start_date = fields.Date(string='Start date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('offered', 'Offered'),
        ('disbursing', 'Disbursing'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', required=True, tracking=True,
       index=True)
    notes = fields.Text(string='Notes')
    schedule_line_ids = fields.One2many('sf.loan.schedule.line', 'loan_id',
                                        string='Amortization schedule')
    disbursement_ids = fields.One2many('sf.loan.disbursement', 'loan_id',
                                       string='Drawdowns')
    repayment_ids = fields.One2many('sf.loan.repayment', 'loan_id',
                                    string='Early repayments')
    covenant_ids = fields.One2many('sf.loan.covenant', 'loan_id',
                                   string='Covenants')
    disbursed_amount = fields.Float(string='Disbursed', compute='_compute_disbursed',
                                    store=True)
    paid_amount = fields.Float(string='Principal paid', compute='_compute_paid',
                               store=True)
    repayment_total = fields.Float(string='Early repayments',
                                   compute='_compute_repayment_total',
                                   store=True)
    remaining_balance = fields.Float(string='Remaining balance',
                                     compute='_compute_remaining', store=True)
    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.company,
                                 required=True)

    @api.depends('disbursement_ids.amount')
    def _compute_disbursed(self):
        for loan in self:
            loan.disbursed_amount = round(
                sum(loan.disbursement_ids.mapped('amount')), 2)

    @api.depends('schedule_line_ids.principal', 'schedule_line_ids.paid')
    def _compute_paid(self):
        for loan in self:
            loan.paid_amount = round(
                sum(line.principal for line in loan.schedule_line_ids
                    if line.paid), 2)

    @api.depends('repayment_ids.amount')
    def _compute_repayment_total(self):
        for loan in self:
            loan.repayment_total = round(
                sum(loan.repayment_ids.mapped('amount')), 2)

    @api.depends('amount', 'schedule_line_ids.principal',
                 'schedule_line_ids.paid', 'repayment_ids.amount')
    def _compute_remaining(self):
        for loan in self:
            paid = sum(line.principal for line in loan.schedule_line_ids
                       if line.paid)
            repaid = sum(loan.repayment_ids.mapped('amount'))
            loan.remaining_balance = round(loan.amount - paid - repaid, 2)

    @api.model
    def create(self, vals):
        if not vals.get('name'):
            seq = self.env['ir.sequence'].next_by_code('sf.loan')
            vals['name'] = 'LOA-%s' % seq
        return super().create(vals)

    def _add_months(self, date, months):
        month_index = date.month - 1 + months
        year = date.year + month_index // 12
        month = month_index % 12 + 1
        day = min(date.day, calendar.monthrange(year, month)[1])
        return date.replace(year=year, month=month, day=day)

    def _generate_schedule_lines(self, amount, months):
        self.ensure_one()
        vals_list = []
        remaining = amount
        total_principal = 0.0
        r = self.rate / 100.0 / 12.0
        payment = 0.0
        if self.amortization == 'annuity':
            if r:
                payment = amount * r / (1 - (1 + r) ** (-months))
            else:
                payment = amount / months
        due = self.start_date or fields.Date.today()
        for i in range(1, months + 1):
            interest = round(remaining * r, 2)
            if i == months:
                principal = round(amount - total_principal, 2)
            elif self.amortization == 'annuity':
                principal = round(payment - interest, 2)
            else:
                principal = round(amount / months, 2)
            principal = max(principal, 0.0)
            total = round(principal + interest, 2)
            total_principal = round(total_principal + principal, 2)
            vals_list.append({
                'loan_id': self.id,
                'line_number': i,
                'due_date': due,
                'principal': principal,
                'interest': interest,
                'total': total,
            })
            remaining = round(remaining - principal, 2)
            if i < months:
                due = self._add_months(due, 1)
        self.env['sf.loan.schedule.line'].create(vals_list)

    def action_generate_schedule(self):
        self.ensure_one()
        if not self.amount or not self.term_months:
            raise UserError(_('Amount and term are required to generate '
                              'a schedule.'))
        self.schedule_line_ids.unlink()
        self._generate_schedule_lines(self.amount, self.term_months)

    def action_offer(self):
        self.ensure_one()
        if self.state != 'draft':
            raise UserError(_('Only draft loans can be offered.'))
        self.state = 'offered'

    def action_disburse(self):
        self.ensure_one()
        if self.state in ('draft', 'offered'):
            self.state = 'disbursing'
        unpaid = self.schedule_line_ids.filtered(lambda line: not line.paid)
        if unpaid:
            self.schedule_line_ids = [(2, line.id) for line in unpaid]
            self._generate_schedule_lines(self.remaining_balance,
                                          len(unpaid))
        if self.disbursed_amount >= self.amount:
            self.state = 'active'

    def _apply_early_repayment(self, amount):
        self.ensure_one()
        outstanding = self.amount - self.paid_amount - (
            self.repayment_total - amount)
        if amount > outstanding + 0.01:
            raise UserError(_('The repayment amount exceeds the remaining '
                              'balance of the loan.'))
        unpaid = self.schedule_line_ids.filtered(
            lambda line: not line.paid).sorted(key=lambda line: line.line_number)
        if not unpaid:
            return
        last = unpaid[-1]
        new_principal = max(round(last.principal - amount, 2), 0.0)
        last.write({
            'principal': new_principal,
            'total': round(new_principal + last.interest, 2),
        })
        if new_principal == 0.0:
            last.paid = True

    def action_close(self):
        self.ensure_one()
        if not self.env.user.has_group('sf_bank_loans.group_loan_manager'):
            raise UserError(_('Only loan managers can close loans.'))
        self.state = 'closed'

    def _check_loan_alerts(self):
        companies = self.env['res.company'].search([])
        today = fields.Date.context_today(self)
        for company in companies:
            loans = self.with_company(company.id).search([])
            for loan in loans:
                for covenant in loan.covenant_ids.filtered(
                        lambda cov: cov.state == 'active'):
                    if covenant.current_value is not False and (
                            covenant.current_value < covenant.target_min
                            or covenant.current_value > covenant.target_max):
                        covenant.state = 'breached'
                        existing = covenant.activity_ids.filtered(
                            lambda act: act.activity_type_id.xml_id
                            == 'mail.mail_activity_data_todo'
                            and act.state != 'done')
                        if existing:
                            continue
                        covenant.activity_schedule(
                            'mail.mail_activity_data_todo',
                            summary=_('Covenant breached: %s')
                            % (covenant.covenant_name or covenant.name),
                            user_id=self.env.user.id)
                alert_date = today - timedelta(
                    days=company.sf_loan_alert_days)
                for line in loan.schedule_line_ids.filtered(
                        lambda ln: not ln.paid and ln.due_date
                        and ln.due_date < alert_date):
                    existing = line.activity_ids.filtered(
                        lambda act: act.activity_type_id.xml_id
                        == 'mail.mail_activity_data_todo'
                        and act.state != 'done')
                    if existing:
                        continue
                    line.activity_schedule(
                        'mail.mail_activity_data_todo',
                        summary=_('Overdue installment: %s') % loan.name,
                        user_id=self.env.user.id)