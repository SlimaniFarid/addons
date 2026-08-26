# -*- coding: utf-8 -*-
from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestTradeFinance(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Instrument = self.env['sf.trade.instrument']
        self.Bank = self.env['sf.trade.bank']
        self.group_user = self.env.ref('sf_trade_finance.group_trade_user')
        self.group_manager = self.env.ref(
            'sf_trade_finance.group_trade_manager')
        self.env.user.groups_id += self.group_manager

    def _create_bank(self):
        return self.Bank.create({'name': 'Test Bank'})

    def _create_counterparty(self):
        return self.env['res.partner'].create({'name': 'Counterparty'})

    def _create_instrument(self, instrument_type='import_lc'):
        return self.Instrument.create({
            'instrument_type': instrument_type,
            'direction': 'import',
            'bank_id': self._create_bank().id,
            'counterparty_id': self._create_counterparty().id,
            'amount': 50000.0,
            'application_date': fields.Date.today(),
            'expiry_date': fields.Date(2027, 12, 31),
        })

    def test_name_sequence(self):
        instrument = self._create_instrument('import_lc')
        self.assertTrue(instrument.name.startswith('LC-'))

    def test_workflow(self):
        instrument = self._create_instrument()
        instrument.action_request()
        self.assertEqual(instrument.state, 'requested')
        instrument.action_issue()
        self.assertEqual(instrument.state, 'issued')
        instrument.action_activate()
        self.assertEqual(instrument.state, 'active')

    def test_settle_requires_documents_accepted(self):
        instrument = self._create_instrument()
        instrument.action_request()
        instrument.action_issue()
        instrument.action_activate()
        self.env['sf.trade.instrument.document'].create({
            'instrument_id': instrument.id,
            'name': 'Bill of Lading',
        })
        with self.assertRaises(UserError):
            instrument.action_settle()

    def test_settle_with_accepted_documents(self):
        instrument = self._create_instrument()
        instrument.action_request()
        instrument.action_issue()
        instrument.action_activate()
        doc = self.env['sf.trade.instrument.document'].create({
            'instrument_id': instrument.id,
            'name': 'Bill of Lading',
        })
        doc.action_submit()
        doc.action_accept()
        instrument.action_settle()
        self.assertEqual(instrument.state, 'settled')
        self.assertTrue(instrument.payment_date)

    def test_settle_without_documents_allowed(self):
        instrument = self._create_instrument()
        instrument.action_request()
        instrument.action_issue()
        instrument.action_activate()
        instrument.action_settle()
        self.assertEqual(instrument.state, 'settled')

    def test_expiry_before_issue(self):
        instrument = self.Instrument.create({
            'instrument_type': 'import_lc',
            'direction': 'import',
            'bank_id': self._create_bank().id,
            'counterparty_id': self._create_counterparty().id,
            'amount': 1000.0,
            'issue_date': fields.Date.today(),
            'expiry_date': fields.Date.today(),
        })
        with self.assertRaises(ValidationError):
            instrument.write({
                'issue_date': fields.Date(2026, 12, 31),
                'expiry_date': fields.Date(2026, 1, 1),
            })

    def test_cron_expiry_alert(self):
        self.env['res.users'].create({
            'name': 'Trade Manager',
            'login': 'trade_manager_user',
            'groups_id': [(6, 0, [self.group_user.id,
                                  self.group_manager.id])],
        })
        instrument = self._create_instrument()
        instrument.action_request()
        instrument.action_issue()
        instrument.action_activate()
        self.env.company.sf_trade_alert_days = 30
        instrument.expiry_date = fields.Date.today()
        instrument._check_trade_expiry_alerts()
        self.assertTrue(instrument.activity_ids)

    def test_unique_name(self):
        bank = self._create_bank()
        partner = self._create_counterparty()
        common = {
            'direction': 'import',
            'bank_id': bank.id,
            'counterparty_id': partner.id,
            'amount': 1000.0,
        }
        first = self.Instrument.create(dict(common, name='LC-DUP'))
        with self.assertRaises(Exception):
            self.Instrument.create(dict(common, name='LC-DUP'))

    def test_active_instrument_cannot_be_deleted(self):
        instrument = self._create_instrument()
        instrument.action_request()
        instrument.action_issue()
        instrument.action_activate()
        with self.assertRaises(UserError):
            instrument.unlink()

    def test_cancel_wizard(self):
        instrument = self._create_instrument()
        wizard = self.env['sf.trade.instrument.cancel.wizard'].create({
            'instrument_id': instrument.id,
            'reason': 'Supplier changed terms.',
        })
        wizard.action_confirm()
        self.assertEqual(instrument.state, 'cancelled')

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Trade Company B'})
        user = self.env['res.users'].create({
            'name': 'Trade Company A User',
            'login': 'trade_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        other = self.Instrument.with_company(company_b).create({
            'instrument_type': 'import_lc',
            'direction': 'import',
            'bank_id': self._create_bank().id,
            'counterparty_id': self._create_counterparty().id,
            'amount': 5000.0,
        })
        self.assertNotIn(other, self.Instrument.with_user(user).search(
            [('id', '=', other.id)]))