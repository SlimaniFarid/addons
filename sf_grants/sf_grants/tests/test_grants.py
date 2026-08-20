# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestGrants(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Program = self.env['sf.grant.program']
        self.Call = self.env['sf.grant.call']
        self.Application = self.env['sf.grant.application']
        self.Expense = self.env['sf.grant.expense']
        self.group_user = self.env.ref('sf_grants.group_grant_user')
        self.group_manager = self.env.ref('sf_grants.group_grant_manager')
        self.env.user.groups_id += self.group_manager

    def _create_program(self):
        return self.Program.create({
            'funder': 'European Commission',
            'funder_type': 'european',
        })

    def _create_call(self, program=None, deadline=None, state='open'):
        return self.Call.create({
            'program_id': (program or self._create_program()).id,
            'title': 'Horizon Grant',
            'budget': 100000.0,
            'open_date': date.today() - timedelta(days=10),
            'deadline_date': deadline or date.today() + timedelta(days=30),
            'max_amount': 50000.0,
            'state': state,
        })

    def _create_application(self, call=None, requested=10000.0,
                            state='draft'):
        return self.Application.create({
            'call_id': (call or self._create_call()).id,
            'title': 'Research Project',
            'applicant': 'Acme Labs',
            'requested_amount': requested,
            'state': state,
        })

    def _create_expense(self, app=None, amount=1000.0, state='claimed',
                        justification='INV-001'):
        return self.Expense.create({
            'application_id': (app or self._create_application()).id,
            'expense_date': date.today(),
            'category': 'equipment',
            'amount': amount,
            'justification': justification,
            'state': state,
        })

    def test_sequence_prefixes(self):
        program = self._create_program()
        call = self._create_call(program=program)
        app = self._create_application(call=call)
        expense = self._create_expense(app=app)
        self.assertTrue(program.name.startswith('PRG-'))
        self.assertTrue(call.name.startswith('CAL-'))
        self.assertTrue(app.name.startswith('APP-'))
        self.assertTrue(expense.name.startswith('EXP-'))

    def test_full_application_workflow(self):
        app = self._create_application()
        app.action_submit()
        self.assertEqual(app.state, 'submitted')
        self.assertTrue(app.submission_date)
        app.action_approve()
        self.assertEqual(app.state, 'approved')
        self.assertEqual(app.granted_amount, app.requested_amount)
        self.assertTrue(app.decision_date)
        app.action_pay()
        self.assertEqual(app.state, 'paid')
        app.action_close()
        self.assertEqual(app.state, 'closed')

    def test_submit_without_call(self):
        app = self.Application.create({
            'title': 'No Call',
            'applicant': 'Acme Labs',
            'requested_amount': 1000.0,
        })
        with self.assertRaises(UserError):
            app.action_submit()

    def test_submit_without_amount(self):
        app = self.Application.create({
            'call_id': self._create_call().id,
            'title': 'No Amount',
            'applicant': 'Acme Labs',
        })
        with self.assertRaises(UserError):
            app.action_submit()

    def test_expense_validate_requires_justification(self):
        app = self._create_application()
        expense = self._create_expense(app=app, justification=False,
                                       state='draft')
        expense.action_claim()
        self.assertEqual(expense.state, 'claimed')
        with self.assertRaises(UserError):
            expense.action_validate()

    def test_expense_validate_exceeds_granted_amount(self):
        app = self._create_application(requested=5000.0)
        app.action_submit()
        app.action_approve()
        self.assertEqual(app.granted_amount, 5000.0)
        first = self._create_expense(app=app, amount=3000.0,
                                     justification='INV-1', state='draft')
        first.action_claim()
        first.action_validate()
        self.assertEqual(first.state, 'validated')
        second = self._create_expense(app=app, amount=3000.0,
                                      justification='INV-2', state='draft')
        second.action_claim()
        with self.assertRaises(UserError):
            second.action_validate()

    def test_cron_deadline_alert_dedup(self):
        program = self._create_program()
        call = self._create_call(program=program, deadline=date.today())
        self.env.company.sf_grant_alert_days = 7
        self.Call._check_grant_alerts()
        self.assertTrue(call.activity_ids)
        count = len(call.activity_ids)
        self.Call._check_grant_alerts()
        self.assertEqual(len(call.activity_ids), count)

    def test_cron_reporting_alert_dedup(self):
        app = self._create_application(requested=1000.0)
        app.action_submit()
        app.action_approve()
        self.assertTrue(app.granted_amount)
        self.Call._check_grant_alerts()
        self.assertTrue(app.activity_ids)
        count = len(app.activity_ids)
        self.Call._check_grant_alerts()
        self.assertEqual(len(app.activity_ids), count)

    def test_multi_company_rule(self):
        self._create_program()
        company_b = self.env['res.company'].create(
            {'name': 'Grants Company B'})
        user = self.env['res.users'].create({
            'name': 'Grants Company A User',
            'login': 'grants_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        program_b = self.Program.with_company(company_b).create({
            'funder': 'Regional Council',
            'funder_type': 'regional',
        })
        call_b = self.Call.with_company(company_b).create({
            'program_id': program_b.id,
            'title': 'Regional Call',
        })
        other = self.Application.with_company(company_b).create({
            'call_id': call_b.id,
            'title': 'Other Company App',
            'applicant': 'Other Corp',
            'requested_amount': 100.0,
        })
        self.assertNotIn(other, self.Application.with_user(user).search(
            [('id', '=', other.id)]))

    def test_report_records_exist(self):
        report_financial = self.env.ref('sf_grants.report_financial')
        report_aid_register = self.env.ref('sf_grants.report_aid_register')
        self.assertEqual(report_financial.model, 'sf.grant.program')
        self.assertEqual(report_aid_register.model, 'sf.grant.application')
        self.assertTrue(self.env.ref('sf_grants.report_financial_template'))
        self.assertTrue(
            self.env.ref('sf_grants.report_aid_register_template'))