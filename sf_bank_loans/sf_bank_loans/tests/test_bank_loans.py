# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestBankLoans(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Bank = self.env['sf.loan.bank']
        self.Loan = self.env['sf.loan']
        self.Disbursement = self.env['sf.loan.disbursement']
        self.Repayment = self.env['sf.loan.repayment']
        self.Covenant = self.env['sf.loan.covenant']
        self.group_user = self.env.ref('sf_bank_loans.group_loan_user')
        self.group_manager = self.env.ref('sf_bank_loans.group_loan_manager')
        self.env.user.groups_id = (
            self.env.user.groups_id | self.group_user | self.group_manager)

    def _create_bank(self):
        return self.Bank.create({})

    def _create_loan(self, amount=1200.0, rate=6.0, term_months=12,
                     amortization='annuity'):
        bank = self._create_bank()
        return self.Loan.create({
            'bank_id': bank.id,
            'amount': amount,
            'rate': rate,
            'term_months': term_months,
            'amortization': amortization,
            'start_date': fields.Date.today(),
        })

    def test_sequences_prefixes(self):
        bank = self._create_bank()
        self.assertTrue(bank.name.startswith('BNK-'))
        loan = self._create_loan()
        self.assertTrue(loan.name.startswith('LOA-'))
        disbursement = self.Disbursement.create({
            'loan_id': loan.id,
            'amount': 500.0,
            'date': fields.Date.today(),
        })
        self.assertTrue(disbursement.name.startswith('DIS-'))
        repayment = self.Repayment.create({
            'loan_id': loan.id,
            'amount': 100.0,
            'date': fields.Date.today(),
        })
        self.assertTrue(repayment.name.startswith('REP-'))
        covenant = self.Covenant.create({
            'loan_id': loan.id,
            'covenant_name': 'Debt ratio',
            'metric': 'debt_ratio',
            'target_min': 1.0,
            'target_max': 2.0,
            'current_value': 1.5,
        })
        self.assertTrue(covenant.name.startswith('COV-'))

    def test_annuity_schedule_math(self):
        loan = self._create_loan()
        loan.action_generate_schedule()
        self.assertEqual(len(loan.schedule_line_ids), 12)
        self.assertEqual(
            round(sum(loan.schedule_line_ids.mapped('principal')), 2), 1200.0)

    def test_constant_schedule_math(self):
        loan = self._create_loan(amortization='constant')
        loan.action_generate_schedule()
        lines = loan.schedule_line_ids.sorted(
            key=lambda line: line.line_number)
        self.assertEqual(len(lines), 12)
        self.assertEqual(
            round(sum(lines.mapped('principal')), 2), 1200.0)
        for line in lines[:11]:
            self.assertEqual(line.principal, 100.0)

    def test_disbursement_updates_balance_and_schedule(self):
        loan = self._create_loan()
        loan.action_generate_schedule()
        disbursement = self.Disbursement.create({
            'loan_id': loan.id,
            'amount': 600.0,
            'date': fields.Date.today(),
        })
        self.assertTrue(disbursement.name.startswith('DIS-'))
        self.assertEqual(loan.disbursed_amount, 600.0)
        self.assertEqual(loan.state, 'disbursing')
        self.assertEqual(len(loan.schedule_line_ids), 12)
        self.assertEqual(
            round(sum(loan.schedule_line_ids.mapped('principal')), 2), 1200.0)
        self.Disbursement.create({
            'loan_id': loan.id,
            'amount': 600.0,
            'date': fields.Date.today(),
        })
        self.assertEqual(loan.disbursed_amount, 1200.0)
        self.assertEqual(loan.state, 'active')

    def test_early_repayment_reduces_balance(self):
        loan = self._create_loan()
        loan.action_generate_schedule()
        repayment = self.Repayment.create({
            'loan_id': loan.id,
            'amount': 100.0,
            'date': fields.Date.today(),
        })
        repayment.action_confirm()
        self.assertTrue(repayment.name.startswith('REP-'))
        self.assertEqual(repayment.state, 'done')
        self.assertEqual(loan.remaining_balance, 1100.0)
        self.assertEqual(loan.repayment_total, 100.0)

    def test_covenant_breach_and_cron_alert_dedup(self):
        loan = self._create_loan()
        loan.action_generate_schedule()
        covenant = self.Covenant.create({
            'loan_id': loan.id,
            'covenant_name': 'Debt ratio',
            'metric': 'debt_ratio',
            'target_min': 1.0,
            'target_max': 2.0,
            'current_value': 5.0,
        })
        loan._check_loan_alerts()
        self.assertEqual(covenant.state, 'breached')
        self.assertTrue(covenant.activity_ids)
        self.assertEqual(len(covenant.activity_ids), 1)
        covenant.state = 'active'
        loan._check_loan_alerts()
        self.assertEqual(covenant.state, 'breached')
        self.assertEqual(len(covenant.activity_ids), 1)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Loan Company B'})
        user = self.env['res.users'].create({
            'name': 'Loan Company A User',
            'login': 'loan_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        bank = self.Bank.with_company(company_b).create({'name': 'Bank B'})
        other = self.Loan.with_company(company_b).create({
            'bank_id': bank.id,
            'amount': 1000.0,
            'rate': 5.0,
            'term_months': 6,
            'amortization': 'annuity',
            'start_date': fields.Date.today(),
        })
        self.assertNotIn(other, self.Loan.with_user(user).search(
            [('id', '=', other.id)]))

    def test_reports_exist(self):
        report = self.env.ref('sf_bank_loans.report_loan_amortization')
        self.assertEqual(report.model, 'sf.loan')
        self.assertEqual(
            report.report_name,
            'sf_bank_loans.report_amortization_template')
        debt = self.env.ref('sf_bank_loans.report_loan_debt_position')
        self.assertEqual(debt.model, 'sf.loan.bank')
        self.assertEqual(
            debt.report_name,
            'sf_bank_loans.report_debt_position_template')