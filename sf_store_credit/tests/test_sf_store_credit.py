# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields as odoo_fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfStoreCredit(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })
        self.account = self.env['sf.store.credit.account'].create({
            'partner_id': self.customer.id,
        })

    def _create_credit(self, amount=100.0, **kw):
        vals = {
            'account_id': self.account.id,
            'amount': amount,
            'reason': 'Goodwill gesture',
        }
        vals.update(kw)
        return self.env['sf.store.credit'].create(vals)

    def test_sequences(self):
        self.assertTrue(self.account.name.startswith('SCA-'))
        credit = self._create_credit()
        self.assertTrue(credit.name.startswith('SCT-'))
        credit.action_confirm()
        self.assertTrue(credit.move_ids[0].name.startswith('SCM-'))

    def test_account_unique_partner(self):
        with self.assertRaises(Exception):
            self.env['sf.store.credit.account'].create({'partner_id': self.customer.id})

    def test_grant_increases_balance(self):
        credit = self._create_credit(amount=100.0)
        self.assertEqual(self.account.balance, 0.0)
        credit.action_confirm()
        self.assertEqual(self.account.balance, 100.0)

    def test_partial_use(self):
        credit = self._create_credit(amount=100.0)
        credit.action_confirm()
        credit.action_use(30.0)
        self.assertEqual(credit.used_amount, 30.0)
        self.assertEqual(credit.remaining, 70.0)
        self.assertEqual(self.account.balance, 70.0)
        self.assertEqual(credit.state, 'confirmed')

    def test_full_use(self):
        credit = self._create_credit(amount=100.0)
        credit.action_confirm()
        credit.action_use(100.0)
        self.assertEqual(credit.state, 'used')
        self.assertEqual(credit.remaining, 0.0)
        self.assertEqual(self.account.balance, 0.0)

    def test_use_beyond_remaining(self):
        credit = self._create_credit(amount=100.0)
        credit.action_confirm()
        with self.assertRaises(UserError):
            credit.action_use(150.0)

    def test_use_draft_blocked(self):
        credit = self._create_credit(amount=100.0)
        with self.assertRaises(UserError):
            credit.action_use(10.0)

    def test_use_remaining_button(self):
        credit = self._create_credit(amount=100.0)
        credit.action_confirm()
        credit.action_use(40.0)
        credit.action_use_remaining()
        self.assertEqual(credit.state, 'used')
        self.assertEqual(credit.remaining, 0.0)

    def test_expiration_cron(self):
        credit = self._create_credit(amount=100.0,
                                     expiration_date=odoo_fields.Date.today() - timedelta(days=1))
        credit.action_confirm()
        self.env['sf.store.credit']._cron_daily_checks()
        self.assertEqual(credit.state, 'expired')
        self.assertEqual(self.account.balance, 0.0)
        with self.assertRaises(UserError):
            credit.action_use(10.0)

    def test_expiry_reminder_activity(self):
        self.env['ir.config_parameter'].set_param('sf_store_credit.expiry_reminder_days', '7')
        credit = self._create_credit(amount=100.0,
                                     expiration_date=odoo_fields.Date.today() + timedelta(days=3))
        credit.action_confirm()
        self.env['sf.store.credit']._cron_daily_checks()
        self.assertEqual(credit.state, 'confirmed')
        self.assertTrue(credit.activity_ids)

    def test_adjustment(self):
        credit = self._create_credit(amount=100.0)
        credit.action_confirm()
        credit.action_adjust(40.0, 'Correction')
        self.assertEqual(credit.used_amount, 40.0)
        self.assertEqual(credit.remaining, 60.0)
        self.assertEqual(self.account.balance, 60.0)
        credit.action_adjust(60.0, 'Full correction')
        self.assertEqual(credit.state, 'adjusted')
        self.assertEqual(credit.remaining, 0.0)

    def test_adjustment_beyond_remaining(self):
        credit = self._create_credit(amount=100.0)
        credit.action_confirm()
        with self.assertRaises(UserError):
            credit.action_adjust(150.0, 'Too much')

    def test_cancel_draft(self):
        credit = self._create_credit(amount=100.0)
        credit.action_cancel()
        self.assertEqual(credit.state, 'cancelled')
        self.assertEqual(self.account.balance, 0.0)

    def test_cancel_used_blocked(self):
        credit = self._create_credit(amount=100.0)
        credit.action_confirm()
        credit.action_use(30.0)
        with self.assertRaises(UserError):
            credit.action_cancel()

    def test_workflow(self):
        credit = self._create_credit(amount=50.0)
        self.assertEqual(credit.state, 'draft')
        credit.action_confirm()
        self.assertEqual(credit.state, 'confirmed')
        credit.action_use(50.0)
        self.assertEqual(credit.state, 'used')

    def test_permissions(self):
        user = self.env['res.users'].create({
            'name': 'Credit User %s' % uuid.uuid4().hex[:4],
            'login': 'cr_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_store_credit.group_sf_store_credit_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        credit = self._create_credit(amount=100.0)
        with self.assertRaises(UserError):
            credit.with_user(user).action_confirm()
        credit.action_confirm()
        with self.assertRaises(UserError):
            credit.with_user(user).action_adjust(10.0, 'Blocked')
        with self.assertRaises(UserError):
            credit.with_user(user).action_cancel()
        created = self.env['sf.store.credit'].with_user(user).create({
            'account_id': self.account.id,
            'amount': 25.0,
            'reason': 'User granted',
        })
        self.assertTrue(created)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Credit Co 2'})
        customer2 = self.env['res.partner'].create({'name': 'Customer 2 %s' % uuid.uuid4().hex[:4]})
        account2 = self.env['sf.store.credit.account'].with_company(company2).create({
            'partner_id': customer2.id,
            'company_id': company2.id,
        })
        credit2 = self.env['sf.store.credit'].with_company(company2).create({
            'account_id': account2.id,
            'amount': 75.0,
            'reason': 'Test',
        })
        self.assertEqual(credit2.company_id, company2)
        user = self.env['res.users'].create({
            'name': 'Credit User %s' % uuid.uuid4().hex[:4],
            'login': 'cr_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_store_credit.group_sf_store_credit_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.store.credit.account'].with_user(user).search(
            [('id', '=', account2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        credit = self._create_credit(amount=100.0)
        credit.action_confirm()
        credit.action_use(30.0)
        action = self.env.ref(
            'sf_store_credit.action_report_store_credit_account').report_action(self.account)
        self.assertTrue(action)
        action = self.env.ref(
            'sf_store_credit.action_report_store_credit').report_action(credit)
        self.assertTrue(action)