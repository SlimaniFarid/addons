# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields as odoo_fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfTradePromotions(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def _create_program(self, budget=1000.0, days_start=-5, days_end=10, state=None, **kw):
        vals = {
            'name': 'Program %s' % uuid.uuid4().hex[:6],
            'start_date': odoo_fields.Date.today() + timedelta(days=days_start),
            'end_date': odoo_fields.Date.today() + timedelta(days=days_end),
            'budget': budget,
        }
        vals.update(kw)
        program = self.env['sf.trade.program'].create(vals)
        if state:
            getattr(program, 'action_%s' % state)()
        return program

    def _create_claim(self, program, amount=100.0, **kw):
        vals = {
            'program_id': program.id,
            'partner_id': self.customer.id,
            'amount': amount,
        }
        vals.update(kw)
        return self.env['sf.trade.claim'].create(vals)

    def test_sequences(self):
        program = self._create_program()
        self.assertTrue(program.name.startswith('TPR-'))
        claim = self._create_claim(program)
        self.assertTrue(claim.name.startswith('TCL-'))

    def test_program_workflow(self):
        program = self._create_program()
        self.assertEqual(program.state, 'draft')
        program.action_activate()
        self.assertEqual(program.state, 'active')
        program.action_close()
        self.assertEqual(program.state, 'closed')
        program2 = self._create_program()
        program2.action_activate()
        program2.action_cancel()
        self.assertEqual(program2.state, 'cancelled')

    def test_activate_blocked_on_non_draft(self):
        program = self._create_program(state='active')
        with self.assertRaises(UserError):
            program.action_activate()

    def test_activate_invalid_dates(self):
        program = self._create_program(days_start=10, days_end=-5)
        with self.assertRaises(UserError):
            program.action_activate()

    def test_close_blocked_on_non_active(self):
        program = self._create_program()
        with self.assertRaises(UserError):
            program.action_close()

    def test_claim_workflow(self):
        program = self._create_program(state='active')
        claim = self._create_claim(program)
        self.assertEqual(claim.state, 'draft')
        claim.action_submit()
        self.assertEqual(claim.state, 'submitted')
        claim.action_approve()
        self.assertEqual(claim.state, 'approved')
        claim.action_mark_paid()
        self.assertEqual(claim.state, 'paid')
        with self.assertRaises(UserError):
            claim.action_cancel()

    def test_reject_and_cancel(self):
        program = self._create_program(state='active')
        claim = self._create_claim(program)
        claim.action_submit()
        claim.action_reject()
        self.assertEqual(claim.state, 'rejected')
        claim.action_cancel()
        self.assertEqual(claim.state, 'cancelled')

    def test_submit_requires_active_program(self):
        program = self._create_program()
        claim = self._create_claim(program)
        with self.assertRaises(UserError):
            claim.action_submit()

    def test_budget_guard(self):
        program = self._create_program(budget=1000.0, state='active')
        claim = self._create_claim(program, amount=1000.0)
        claim.action_submit()
        claim.action_approve()
        claim2 = self._create_claim(program, amount=100.0)
        claim2.action_submit()
        with self.assertRaises(UserError):
            claim2.action_approve()

    def test_computed_amounts(self):
        program = self._create_program(budget=1000.0, state='active')
        claim = self._create_claim(program, amount=250.0)
        self.assertEqual(program.total_claimed, 0.0)
        self.assertEqual(program.remaining_budget, 1000.0)
        claim.action_submit()
        claim.action_approve()
        self.assertEqual(program.total_claimed, 250.0)
        self.assertEqual(program.remaining_budget, 750.0)
        self.assertAlmostEqual(program.roi, 25.0)

    def test_cron_closes_expired(self):
        program = self._create_program(state='active', days_end=-1)
        self.env['sf.trade.program']._cron_daily_checks()
        self.assertEqual(program.state, 'closed')

    def test_threshold_activity(self):
        self.env['ir.config_parameter'].set_param(
            'sf_trade_promotions.validation_threshold', '500')
        program = self._create_program(state='active')
        claim = self._create_claim(program, amount=700.0)
        claim.action_submit()
        self.assertTrue(claim.activity_ids)
        low = self._create_claim(program, amount=50.0)
        low.action_submit()
        self.assertFalse(low.activity_ids)

    def test_permissions(self):
        user = self.env['res.users'].create({
            'name': 'Trade User %s' % uuid.uuid4().hex[:4],
            'login': 'tr_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_trade_promotions.group_sf_trade_promotions_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        program = self._create_program(state='active')
        claim = self._create_claim(program)
        claim.action_submit()
        with self.assertRaises(UserError):
            claim.with_user(user).action_approve()
        with self.assertRaises(UserError):
            program.with_user(user).action_close()
        created = self.env['sf.trade.claim'].with_user(user).create({
            'program_id': program.id,
            'partner_id': self.customer.id,
            'amount': 10.0,
        })
        self.assertTrue(created)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Trade Co 2'})
        customer2 = self.env['res.partner'].create({'name': 'Customer 2 %s' % uuid.uuid4().hex[:4]})
        program2 = self.env['sf.trade.program'].with_company(company2).create({
            'name': 'Program Co2 %s' % uuid.uuid4().hex[:4],
            'start_date': odoo_fields.Date.today() - timedelta(days=2),
            'end_date': odoo_fields.Date.today() + timedelta(days=5),
            'budget': 500.0,
            'company_id': company2.id,
        })
        claim2 = self.env['sf.trade.claim'].with_company(company2).create({
            'program_id': program2.id,
            'partner_id': customer2.id,
            'amount': 50.0,
        })
        self.assertEqual(claim2.company_id, company2)
        user = self.env['res.users'].create({
            'name': 'Trade User %s' % uuid.uuid4().hex[:4],
            'login': 'tr_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_trade_promotions.group_sf_trade_promotions_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.trade.program'].with_user(user).search(
            [('id', '=', program2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        program = self._create_program(state='active')
        claim = self._create_claim(program, amount=100.0)
        claim.action_submit()
        claim.action_approve()
        action = self.env.ref(
            'sf_trade_promotions.action_report_trade_program').report_action(program)
        self.assertTrue(action)
        action = self.env.ref(
            'sf_trade_promotions.action_report_trade_claim').report_action(claim)
        self.assertTrue(action)