# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestVendorContracts(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Contract = self.env['sf.vendor.contract']
        self.Version = self.env['sf.vendor.contract.version']
        self.partner = self.env['res.partner'].create({
            'name': 'Test Supplier',
        })
        self.manager = self.env['res.users'].create({
            'name': 'Contracts Manager',
            'login': 'contracts_manager_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref(
                        'sf_vendor_contracts.group_vendor_contracts_manager').id,
                ]),
            ],
        })
        self.user = self.env['res.users'].create({
            'name': 'Contracts User',
            'login': 'contracts_user_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref(
                        'sf_vendor_contracts.group_vendor_contracts_user').id,
                ]),
            ],
        })

    def _make_contract(self, start='2026-01-01', end='2026-12-31', **kw):
        vals = {
            'name': 'Supply Agreement',
            'partner_id': self.partner.id,
            'date_start': start,
            'date_end': end,
            'amount_total': 12000.0,
        }
        vals.update(kw)
        return self.Contract.create(vals)

    def test_01_contract_creation_and_activation(self):
        contract = self._make_contract()
        self.assertEqual(contract.state, 'draft')
        contract.action_activate()
        self.assertEqual(contract.state, 'active')

    def test_02_date_end_before_start_rejected(self):
        with self.assertRaises(UserError):
            self._make_contract(start='2026-12-31', end='2026-01-01')

    def test_03_negative_amount_rejected(self):
        with self.assertRaises(UserError):
            self._make_contract(amount_total=-10.0)

    def test_04_expiring_state_from_cron(self):
        from datetime import date, timedelta
        today = date.today()
        contract = self._make_contract(
            start=(today - timedelta(days=100)).isoformat(),
            end=(today + timedelta(days=30)).isoformat())
        contract.action_activate()
        self.Contract._cron_check_expiration()
        self.assertEqual(contract.state, 'expiring')

    def test_05_expired_state_from_cron(self):
        from datetime import date, timedelta
        today = date.today()
        contract = self._make_contract(
            start=(today - timedelta(days=400)).isoformat(),
            end=(today - timedelta(days=30)).isoformat())
        contract.action_activate()
        self.Contract._cron_check_expiration()
        self.assertEqual(contract.state, 'expired')

    def test_06_no_end_date_never_expires(self):
        contract = self._make_contract(end=False)
        contract.action_activate()
        self.Contract._cron_check_expiration()
        self.assertEqual(contract.state, 'active')

    def test_07_renewal_creates_version(self):
        from datetime import date, timedelta
        today = date.today()
        contract = self._make_contract(
            start=(today - timedelta(days=100)).isoformat(),
            end=(today + timedelta(days=30)).isoformat())
        contract.action_activate()
        contract._create_version('v1')
        versions = self.Version.search([
            ('contract_id', '=', contract.id),
        ])
        self.assertEqual(len(versions), 1)
        self.assertEqual(versions[0].version, 'v1')

    def test_08_renewal_wizard(self):
        from datetime import date, timedelta
        today = date.today()
        contract = self._make_contract(
            start=(today - timedelta(days=100)).isoformat(),
            end=(today + timedelta(days=30)).isoformat())
        contract.action_activate()
        wizard = self.env['sf.vendor.contract.renew.wizard'].create({
            'contract_id': contract.id,
            'new_date_start': today.isoformat(),
            'new_date_end':
                (today + timedelta(days=365)).isoformat(),
            'new_amount': 15000.0,
            'version': 'v2',
        })
        res = wizard.action_renew()
        new_contract = self.env['sf.vendor.contract'].browse(res['res_id'])
        self.assertEqual(contract.state, 'renewed')
        self.assertEqual(new_contract.state, 'active')
        self.assertEqual(new_contract.amount_total, 15000.0)
        self.assertEqual(new_contract.name, 'Supply Agreement (v2)')

    def test_09_renewal_requires_end_date(self):
        contract = self._make_contract()
        contract.action_activate()
        wizard = self.env['sf.vendor.contract.renew.wizard'].create({
            'contract_id': contract.id,
            'new_date_start': '2027-01-01',
            'new_date_end': False,
            'version': 'v2',
        })
        with self.assertRaises(UserError):
            wizard.action_renew()

    def test_10_cancel_workflow(self):
        contract = self._make_contract()
        contract.action_activate()
        wizard = self.env['sf.vendor.contract.cancel.wizard'].create({
            'contract_id': contract.id,
            'reason': 'Contract replaced.',
        })
        wizard.action_cancel()
        self.assertEqual(contract.state, 'cancelled')

    def test_11_user_cannot_cancel(self):
        contract = self._make_contract()
        contract.action_activate()
        with self.assertRaises(UserError):
            contract.with_user(self.user).action_cancel()

    def test_12_clause_and_line_creation(self):
        contract = self._make_contract()
        clause = self.env['sf.vendor.contract.clause'].create({
            'contract_id': contract.id,
            'title': 'Warranty',
            'type': 'warranty',
            'content': '12 months warranty.',
        })
        line = self.env['sf.vendor.contract.line'].create({
            'contract_id': contract.id,
            'description': 'Service',
            'quantity': 10.0,
            'unit_price': 100.0,
        })
        self.assertEqual(clause.contract_id.id, contract.id)
        self.assertEqual(line.amount, 1000.0)

    def test_13_line_amount_computed(self):
        line = self.env['sf.vendor.contract.line'].create({
            'contract_id': self._make_contract().id,
            'description': 'Units',
            'quantity': 5.0,
            'unit_price': 20.0,
        })
        self.assertEqual(line.amount, 100.0)