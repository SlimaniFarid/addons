# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestDebtCollection(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env.ref('base.user_admin')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Debt Customer',
            'credit_limit': 5000.0,
        })

    def _new_case(self, priority='1'):
        return self.env['sf.debt.collection.case'].create({
            'partner_id': self.partner.id,
            'collector_id': self.user.id,
            'priority': priority,
        })

    def test_01_create_case(self):
        case = self._new_case()
        self.assertTrue(case.name)
        self.assertIn('DC/', case.name)
        self.assertEqual(case.state, 'open')
        self.assertEqual(case.partner_id.id, self.partner.id)

    def test_02_workflow(self):
        case = self._new_case()
        case.action_set_in_progress()
        self.assertEqual(case.state, 'in_progress')
        case.action_mark_done()
        self.assertEqual(case.state, 'done')
        case.action_open()
        self.assertEqual(case.state, 'open')
        case.action_cancel()
        self.assertEqual(case.state, 'cancelled')

    def test_03_partner_credit_compute(self):
        self.partner.credit_limit = 5000.0
        self.assertEqual(self.partner.credit_usage, 0.0)
        self.assertEqual(self.partner.credit_available, 5000.0)

    def test_04_promise_flow(self):
        case = self._new_case()
        self.env['sf.debt.promise'].create([
            {'case_id': case.id, 'date': date.today() - timedelta(days=5),
             'amount': 100.0, 'state': 'kept'},
            {'case_id': case.id, 'date': date.today() + timedelta(days=7),
             'amount': 200.0, 'state': 'pending'},
        ])
        self.assertEqual(case.next_promise_date, date.today() + timedelta(days=7))

    def test_05_action_log(self):
        case = self._new_case()
        self.env['sf.debt.action'].create({
            'case_id': case.id,
            'action_type': 'call',
            'summary': 'Called customer, promised payment next week.',
        })
        self.assertEqual(len(case.action_ids), 1)
        self.assertEqual(case.action_ids.action_type, 'call')

    def test_06_dunning_levels(self):
        levels = self.env['sf.debt.dunning'].search([
            ('active', '=', True)], order='sequence asc')
        self.assertEqual(len(levels), 3)
        self.assertEqual(levels[0].days_after_due, 0)
        self.assertEqual(levels[2].days_after_due, 30)

    def test_07_create_dunning_run(self):
        case = self._new_case()
        case.action_create_dunning()
        self.assertEqual(len(case.env['sf.debt.dunning.run'].search([
            ('case_id', '=', case.id)])), 1)
        run = case.env['sf.debt.dunning.run'].search([
            ('case_id', '=', case.id)], limit=1)
        self.assertEqual(run.state, 'draft')
        run.action_sent()
        self.assertEqual(run.state, 'sent')
        run.action_done()
        self.assertEqual(run.state, 'done')

    def test_08_refresh_invoices_no_crash(self):
        case = self._new_case()
        case.action_refresh_invoices()
        self.assertTrue(isinstance(case.total_due, float))