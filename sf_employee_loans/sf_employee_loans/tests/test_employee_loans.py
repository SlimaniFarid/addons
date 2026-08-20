# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestEmployeeLoan(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Loan = self.env['sf.employee.loan']
        self.Line = self.env['sf.employee.loan.line']
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
        })
        self.manager = self.env['res.users'].create({
            'name': 'Manager',
            'login': 'loan_manager_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_employee_loans.group_employee_loans_manager').id,
                ]),
            ],
        })
        self.user = self.env['res.users'].create({
            'name': 'User',
            'login': 'loan_user_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_employee_loans.group_employee_loans_user').id,
                ]),
            ],
        })

    def _make_loan(self, **kw):
        vals = {
            'employee_id': self.employee.id,
            'amount': 1200.0,
            'duration_months': 12,
            'interest_rate': 0.0,
        }
        vals.update(kw)
        return self.Loan.create(vals)

    def test_01_loan_creation_defaults(self):
        loan = self._make_loan()
        self.assertEqual(loan.state, 'draft')
        self.assertEqual(loan.monthly_amount, 100.0)
        self.assertEqual(loan.total_amount, 1200.0)

    def test_02_full_workflow_generates_schedule(self):
        loan = self._make_loan()
        loan.action_submit()
        self.assertEqual(loan.state, 'submitted')
        loan.with_user(self.manager).action_approve()
        self.assertEqual(loan.state, 'approved')
        loan.action_validate()
        self.assertEqual(loan.state, 'active')
        self.assertEqual(len(loan.lines), 12)
        self.assertEqual(sum(l.amount for l in loan.lines), 1200.0)

    def test_03_balance_updates_on_payment(self):
        loan = self._make_loan()
        loan.action_submit()
        loan.with_user(self.manager).action_approve()
        loan.action_validate()
        first = loan.lines[0]
        first.action_record_payment()
        self.assertEqual(loan.paid_amount, 100.0)
        self.assertEqual(loan.balance_due, 1100.0)

    def test_04_close_when_all_paid(self):
        loan = self._make_loan(duration_months=3)
        loan.action_submit()
        loan.with_user(self.manager).action_approve()
        loan.action_validate()
        self.assertEqual(len(loan.lines), 3)
        loan.lines.action_pay_all()
        self.assertEqual(loan.balance_due, 0.0)
        loan.action_close()
        self.assertEqual(loan.state, 'closed')

    def test_05_interest_computation(self):
        loan = self._make_loan(amount=1200.0, interest_rate=6.0,
                               duration_months=12)
        self.assertEqual(loan.total_interest, 72.0)
        self.assertEqual(loan.total_amount, 1272.0)
        self.assertEqual(loan.monthly_amount, 106.0)

    def test_06_non_manager_cannot_approve(self):
        loan = self._make_loan()
        loan.action_submit()
        with self.assertRaises(UserError):
            loan.with_user(self.user).action_approve()

    def test_07_active_loan_cannot_be_deleted(self):
        loan = self._make_loan()
        loan.action_submit()
        loan.with_user(self.manager).action_approve()
        loan.action_validate()
        with self.assertRaises(UserError):
            loan.unlink()

    def test_08_ceiling_enforced(self):
        self.env.company.sf_max_advance = 500.0
        loan = self._make_loan(amount=400.0)
        loan.action_submit()
        loan.with_user(self.manager).action_approve()
        loan.action_validate()
        second = self._make_loan(amount=200.0)
        with self.assertRaises(UserError):
            second.action_submit()

    def test_09_invalid_amount_rejected(self):
        with self.assertRaises(UserError):
            self._make_loan(amount=-10.0)

    def test_10_one_month_edge_case(self):
        loan = self._make_loan(duration_months=1, amount=100.0)
        self.assertEqual(loan.monthly_amount, 100.0)
        loan.action_submit()
        loan.with_user(self.manager).action_approve()
        loan.action_validate()
        self.assertEqual(len(loan.lines), 1)