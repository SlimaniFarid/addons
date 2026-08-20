# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields as odoo_fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfFranchise(TransactionCase):

    def setUp(self):
        super().setUp()
        self.franchisee = self.env['res.partner'].create({
            'name': 'Franchisee %s' % uuid.uuid4().hex[:6],
        })
        self.receivable_account = self.env['account.account'].create({
            'name': 'Franchise Receivable',
            'code': '110000',
            'account_type': 'asset_receivable',
        })
        self.franchisee.property_account_receivable_id = self.receivable_account.id
        self.income_account = self.env['account.account'].create({
            'name': 'Royalty Income',
            'code': '400000',
            'account_type': 'income',
        })
        self.sale_journal = self.env['account.journal'].create({
            'name': 'Franchise Test Sales',
            'type': 'sale',
            'code': 'FSJ',
        })
        self.contract = self.env['sf.franchise.contract'].create({
            'partner_id': self.franchisee.id,
            'territory': 'Paris',
            'royalty_type': 'percentage',
            'royalty_percent': 10.0,
            'start_date': odoo_fields.Date.today(),
        })

    def _create_declaration(self, **kw):
        vals = {
            'contract_id': self.contract.id,
            'period_start': odoo_fields.Date.today() - timedelta(days=30),
            'period_end': odoo_fields.Date.today(),
            'declared_sales': 1000.0,
        }
        vals.update(kw)
        return self.env['sf.franchise.declaration'].create(vals)

    def test_sequences(self):
        self.assertTrue(self.contract.name.startswith('FRC-'))
        declaration = self._create_declaration()
        self.assertTrue(declaration.name.startswith('FRD-'))

    def test_royalty_percentage(self):
        declaration = self._create_declaration(declared_sales=1000.0)
        self.assertEqual(declaration.royalty_amount, 100.0)

    def test_royalty_fixed(self):
        contract = self.env['sf.franchise.contract'].create({
            'partner_id': self.franchisee.id,
            'royalty_type': 'fixed',
            'fixed_amount': 500.0,
            'start_date': odoo_fields.Date.today(),
        })
        declaration = self._create_declaration(contract_id=contract.id, declared_sales=9000.0)
        self.assertEqual(declaration.royalty_amount, 500.0)

    def test_period_validation(self):
        with self.assertRaises(ValidationError):
            self._create_declaration(
                period_start=odoo_fields.Date.today(),
                period_end=odoo_fields.Date.today() - timedelta(days=1),
            )

    def test_declaration_company_propagation(self):
        declaration = self._create_declaration()
        self.assertEqual(declaration.company_id, self.contract.company_id)

    def test_workflow_invoice_paid(self):
        declaration = self._create_declaration()
        self.assertEqual(declaration.state, 'draft')
        declaration.action_confirm()
        self.assertEqual(declaration.state, 'confirmed')
        declaration.action_generate_invoice()
        self.assertEqual(declaration.state, 'invoiced')
        self.assertTrue(declaration.invoice_id)
        self.assertEqual(declaration.invoice_id.move_type, 'out_invoice')
        self.assertEqual(declaration.invoice_id.amount_total, 100.0)
        self.assertEqual(declaration.invoice_id.state, 'posted')
        declaration.action_mark_paid()
        self.assertEqual(declaration.state, 'paid')

    def test_invoice_uses_configured_account_and_journal(self):
        self.env['ir.config_parameter'].set_param(
            'sf_franchise.default_royalty_account_id', str(self.income_account.id))
        self.env['ir.config_parameter'].set_param(
            'sf_franchise.default_sale_journal_id', str(self.sale_journal.id))
        declaration = self._create_declaration()
        declaration.action_confirm()
        declaration.action_generate_invoice()
        invoice = declaration.invoice_id
        self.assertEqual(invoice.journal_id, self.sale_journal)
        line = invoice.line_ids.filtered(lambda l: l.account_id.id == self.income_account.id)
        self.assertTrue(line)

    def test_guard_invoice_unconfirmed(self):
        declaration = self._create_declaration()
        with self.assertRaises(UserError):
            declaration.action_generate_invoice()

    def test_guard_cancel_invoiced(self):
        declaration = self._create_declaration()
        declaration.action_confirm()
        declaration.action_generate_invoice()
        with self.assertRaises(UserError):
            declaration.action_cancel()

    def test_guard_cancel_paid(self):
        declaration = self._create_declaration()
        declaration.action_confirm()
        declaration.action_generate_invoice()
        declaration.action_mark_paid()
        with self.assertRaises(UserError):
            declaration.action_cancel()

    def test_mark_paid_requires_posted_invoice(self):
        declaration = self._create_declaration()
        declaration.action_confirm()
        with self.assertRaises(UserError):
            declaration.action_mark_paid()

    def test_contract_workflow(self):
        self.assertEqual(self.contract.state, 'draft')
        self.contract.action_activate()
        self.assertEqual(self.contract.state, 'active')
        self.contract.action_suspend()
        self.assertEqual(self.contract.state, 'suspended')
        self.contract.action_terminate()
        self.assertEqual(self.contract.state, 'terminated')

    def test_permissions(self):
        user = self.env['res.users'].create({
            'name': 'Franchise User %s' % uuid.uuid4().hex[:4],
            'login': 'fr_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_franchise.group_sf_franchise_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        declaration = self._create_declaration()
        with self.assertRaises(UserError):
            declaration.with_user(user).action_confirm()
        with self.assertRaises(UserError):
            declaration.with_user(user).action_generate_invoice()
        with self.assertRaises(UserError):
            declaration.with_user(user).action_cancel()
        with self.assertRaises(UserError):
            self.contract.with_user(user).action_terminate()

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Franchise Co 2'})
        contract2 = self.env['sf.franchise.contract'].with_company(company2).create({
            'partner_id': self.franchisee.id,
            'royalty_type': 'percentage',
            'royalty_percent': 5.0,
            'start_date': odoo_fields.Date.today(),
            'company_id': company2.id,
        })
        declaration2 = self.env['sf.franchise.declaration'].with_company(company2).create({
            'contract_id': contract2.id,
            'period_start': odoo_fields.Date.today() - timedelta(days=30),
            'period_end': odoo_fields.Date.today(),
            'declared_sales': 2000.0,
        })
        self.assertEqual(declaration2.company_id, company2)
        user = self.env['res.users'].create({
            'name': 'Franchise User %s' % uuid.uuid4().hex[:4],
            'login': 'fr_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_franchise.group_sf_franchise_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.franchise.contract'].with_user(user).search(
            [('id', '=', contract2.id)])
        self.assertFalse(visible)

    def test_cron_reminders(self):
        pending = self._create_declaration()
        pending.action_confirm()
        self.contract.action_activate()
        self.env['sf.franchise.declaration']._cron_daily_checks()
        self.assertTrue(pending.activity_ids)

    def test_report_generation(self):
        declaration = self._create_declaration()
        declaration.action_confirm()
        declaration.action_generate_invoice()
        action = self.env.ref(
            'sf_franchise.action_report_franchise_contract').report_action(self.contract)
        self.assertTrue(action)
        action = self.env.ref(
            'sf_franchise.action_report_franchise_declaration').report_action(declaration)
        self.assertTrue(action)