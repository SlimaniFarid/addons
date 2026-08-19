# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestLitigation(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Case = self.env['sf.litigation.case']
        self.Deadline = self.env['sf.litigation.deadline']
        self.Fee = self.env['sf.litigation.fee']
        self.Decision = self.env['sf.litigation.decision']
        self.group_user = self.env.ref('sf_litigation.group_litigation_user')

    def _create_case(self, state='draft'):
        case = self.Case.create({
            'title': 'Test Case',
            'case_type': 'civil',
        })
        if state in ('opened', 'pending'):
            case.action_open()
        if state == 'pending':
            case.action_pending()
        return case

    def test_create_records_with_sequences(self):
        case = self._create_case()
        self.assertTrue(case.name.startswith('LIT-'))
        deadline = self.Deadline.create({
            'case_id': case.id,
            'deadline_type': 'hearing',
            'due_date': fields.Date.today() + timedelta(days=30),
        })
        self.assertTrue(deadline.name.startswith('DDL-'))
        fee = self.Fee.create({
            'case_id': case.id,
            'fee_type': 'lawyer',
            'amount': 500.0,
            'date': fields.Date.today(),
        })
        self.assertTrue(fee.name.startswith('FEE-'))
        decision = self.Decision.create({
            'case_id': case.id,
            'decision_date': fields.Date.today(),
            'outcome': 'won',
        })
        self.assertTrue(decision.name.startswith('DEC-'))

    def test_missed_deadline(self):
        case = self._create_case()
        deadline = self.Deadline.create({
            'case_id': case.id,
            'deadline_type': 'filing',
            'due_date': fields.Date.today() - timedelta(days=5),
        })
        self.Deadline._check_litigation_deadlines()
        self.assertEqual(deadline.state, 'missed')

    def test_cron_creates_deadline_activity(self):
        case = self._create_case()
        deadline = self.Deadline.create({
            'case_id': case.id,
            'deadline_type': 'response',
            'due_date': fields.Date.today() + timedelta(days=5),
            'alert_days': 10,
        })
        self.Deadline._check_litigation_deadlines()
        self.assertTrue(deadline.activity_ids)
        self.Deadline._check_litigation_deadlines()
        todos = deadline.activity_ids.filtered(
            lambda a: a.activity_type_id ==
            self.env.ref('mail.mail_activity_data_todo')
            and a.state != 'done')
        self.assertEqual(len(todos), 1)

    def test_close_requires_decision_or_reason(self):
        case = self._create_case(state='pending')
        manager = self.env['res.users'].create({
            'name': 'Litigation Manager',
            'login': 'litigation_manager',
            'groups_id': [(4, self.env.ref(
                'sf_litigation.group_litigation_manager').id)],
        })
        case = case.with_user(manager)
        with self.assertRaises(UserError):
            case.action_close()
        case.closed_reason = 'Settled out of court'
        case.action_close()
        self.assertEqual(case.state, 'closed')
        self.assertTrue(case.closed_date)

    def test_close_by_non_manager(self):
        case = self._create_case(state='pending')
        user = self.env['res.users'].create({
            'name': 'Litigation Company A User',
            'login': 'litigation_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        with self.assertRaises(UserError):
            case.with_user(user).action_close()

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({
            'name': 'Litigation Company B'})
        user = self.env['res.users'].create({
            'name': 'Litigation Company A User',
            'login': 'litigation_company_a_user_2',
            'groups_id': [(4, self.group_user.id)],
        })
        self._create_case()
        other = self.Case.with_company(company_b).create({
            'title': 'Case Company B',
            'case_type': 'fiscal',
        })
        self.assertNotIn(other, self.Case.with_user(user).search(
            [('id', '=', other.id)]))

    def test_report_records_exist(self):
        activity = self.env['ir.actions.report'].search([
            ('report_name', '=', 'sf_litigation.report_legal_activity_template')])
        self.assertTrue(activity)
        case_sheet = self.env['ir.actions.report'].search([
            ('report_name', '=', 'sf_litigation.case_sheet_template')])
        self.assertTrue(case_sheet)