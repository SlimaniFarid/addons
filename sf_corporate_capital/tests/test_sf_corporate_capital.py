# -*- coding: utf-8 -*-
import uuid

from odoo import fields as odoo_fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfCorporateCapital(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Partner A'})
        self.user_group = self.env.ref(
            'sf_corporate_capital.group_sf_capital_user')
        self.manager_group = self.env.ref(
            'sf_corporate_capital.group_sf_capital_manager')

    def _create_shareholder(self, **kw):
        vals = {'partner_id': self.partner.id}
        vals.update(kw)
        return self.env['sf.shareholder'].create(vals)

    def _create_share_class(self, **kw):
        vals = {'nominal_value': 10.0, 'authorized_shares': 1000}
        vals.update(kw)
        return self.env['sf.share.class'].create(vals)

    def _create_movement(self, shareholder, share_class, **kw):
        vals = {
            'shareholder_id': shareholder.id,
            'share_class_id': share_class.id,
            'quantity': 100,
            'unit_price': 10.0,
            'date': odoo_fields.Date.today(),
        }
        vals.update(kw)
        return self.env['sf.capital.movement'].create(vals)

    def _create_user(self, group):
        return self.env['res.users'].create({
            'name': 'Capital User',
            'login': 'capital_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [group.id])],
        })

    def test_sequences(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(shareholder, share_class)
        self.assertTrue(shareholder.name.startswith('SHL-'))
        self.assertTrue(share_class.name.startswith('SCL-'))
        self.assertTrue(move.name.startswith('CPM-'))

    def test_amount_compute(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(shareholder, share_class)
        self.assertEqual(move.amount, 1000.0)

    def test_workflow(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(shareholder, share_class)
        move.action_post()
        self.assertEqual(move.state, 'posted')
        move.action_cancel()
        self.assertEqual(move.state, 'cancelled')

    def test_issued_shares(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        buy = self._create_movement(shareholder, share_class)
        buy.action_post()
        self.assertEqual(share_class.issued_shares, 100)
        sell = self._create_movement(
            shareholder, share_class, quantity=30, direction='sell')
        sell.action_post()
        self.assertEqual(share_class.issued_shares, 70)

    def test_shareholder_totals(self):
        holder1 = self._create_shareholder()
        holder2 = self._create_shareholder(name='Holder Two')
        share_class = self._create_share_class()
        buy = self._create_movement(holder1, share_class, quantity=80)
        buy.action_post()
        transfer = self._create_movement(
            holder1, share_class, quantity=20, direction='sell')
        transfer.action_post()
        other = self._create_movement(
            holder2, share_class, quantity=50)
        other.action_post()
        self.assertEqual(holder1.total_shares, 60)
        self.assertEqual(holder1.total_value, 600.0)
        self.assertEqual(holder2.total_shares, 50)

    def test_sell_blocked_when_insufficient(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        sell = self._create_movement(
            shareholder, share_class, quantity=10, direction='sell')
        with self.assertRaises(ValidationError):
            sell.action_post()

    def test_sell_allowed_when_sufficient(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        buy = self._create_movement(shareholder, share_class, quantity=10)
        buy.action_post()
        sell = self._create_movement(
            shareholder, share_class, quantity=10, direction='sell')
        sell.action_post()
        self.assertEqual(sell.state, 'posted')

    def test_state_write_guard(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(shareholder, share_class)
        with self.assertRaises(UserError):
            move.write({'state': 'posted'})

    def test_posted_immutable(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(shareholder, share_class)
        move.action_post()
        with self.assertRaises(UserError):
            move.write({'quantity': 200})

    def test_posted_cancel_manager_only(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(shareholder, share_class)
        move.action_post()
        user = self._create_user(self.user_group)
        with self.assertRaises(UserError):
            move.with_user(user).action_cancel()
        manager = self._create_user(self.manager_group)
        move.with_user(manager).action_cancel()
        self.assertEqual(move.state, 'cancelled')

    def test_negative_quantity_blocked(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                self._create_movement(shareholder, share_class, quantity=-5)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({
            'name': 'Capital Co 2'})
        shareholder2 = self.env['sf.shareholder'].with_company(company2).create({
            'name': 'Co2 Holder',
            'company_id': company2.id,
        })
        user = self._create_user(self.user_group)
        user.write({
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.shareholder'].with_user(user).search(
            [('id', '=', shareholder2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(shareholder, share_class)
        move.action_post()
        cap_action = self.env.ref(
            'sf_corporate_capital.action_report_cap_table').report_action(
            shareholder)
        self.assertTrue(cap_action)
        cert_action = self.env.ref(
            'sf_corporate_capital.action_report_share_certificate').report_action(
            move)
        self.assertTrue(cert_action)