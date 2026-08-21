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
        vals = {'partner_id': self.partner.id, 'shareholder_type': 'individual'}
        vals.update(kw)
        return self.env['sf.shareholder'].create(vals)

    def _create_share_class(self, **kw):
        vals = {'nominal_value': 10.0, 'authorized_shares': 1000}
        vals.update(kw)
        return self.env['sf.share.class'].create(vals)

    def _create_movement(self, **kw):
        """Create a capital movement with flexible parameters.
        
        For issue/buyback: shareholder_id, share_class_id, movement_type
        For transfer: from_shareholder_id, to_shareholder_id, share_class_id
        """
        vals = {
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
        move = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        self.assertTrue(shareholder.name.startswith('SHL-'))
        self.assertTrue(share_class.name.startswith('SCL-'))
        self.assertTrue(move.name.startswith('CPM-'))

    def test_amount_compute(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        self.assertEqual(move.amount, 1000.0)

    def test_workflow(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        move.action_post()
        self.assertEqual(move.state, 'posted')
        move.action_cancel()
        self.assertEqual(move.state, 'cancelled')

    def test_issued_shares(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        buy = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        buy.action_post()
        self.assertEqual(share_class.issued_shares, 100)
        sell = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            quantity=30,
            movement_type='buyback')
        sell.action_post()
        self.assertEqual(share_class.issued_shares, 70)

    def test_shareholder_totals(self):
        holder1 = self._create_shareholder()
        holder2 = self._create_shareholder(name='Holder Two')
        share_class = self._create_share_class()
        buy = self._create_movement(
            shareholder_id=holder1.id,
            share_class_id=share_class.id,
            quantity=80,
            movement_type='issue')
        buy.action_post()
        transfer = self._create_movement(
            from_shareholder_id=holder1.id,
            to_shareholder_id=holder2.id,
            share_class_id=share_class.id,
            quantity=20,
            movement_type='transfer')
        transfer.action_post()
        other = self._create_movement(
            shareholder_id=holder2.id,
            share_class_id=share_class.id,
            quantity=50,
            movement_type='issue')
        other.action_post()
        self.assertEqual(holder1.total_shares, 60)
        self.assertEqual(holder1.total_value, 600.0)
        self.assertEqual(holder2.total_shares, 70)

    def test_buyback_blocked_when_insufficient(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        sell = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            quantity=10,
            movement_type='buyback')
        with self.assertRaises(ValidationError):
            sell.action_post()

    def test_buyback_allowed_when_sufficient(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        buy = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            quantity=10,
            movement_type='issue')
        buy.action_post()
        sell = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            quantity=10,
            movement_type='buyback')
        sell.action_post()
        self.assertEqual(sell.state, 'posted')

    def test_state_write_guard(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        with self.assertRaises(UserError):
            move.write({'state': 'posted'})

    def test_posted_immutable(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        move.action_post()
        with self.assertRaises(UserError):
            move.write({'quantity': 200})

    def test_posted_cancel_manager_only(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        move.action_post()
        user = self._create_user(self.user_group)
        with self.assertRaises(UserError):
            move.with_user(user).action_cancel()
        manager = self._create_user(self.manager_group)
        move.with_user(manager).action_cancel()
        self.assertEqual(move.state, 'cancelled')

    def test_post_manager_only(self):
        """Test that posting requires manager rights."""
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        move = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        user = self._create_user(self.user_group)
        with self.assertRaises(UserError):
            move.with_user(user).action_post()
        manager = self._create_user(self.manager_group)
        move.with_user(manager).action_post()
        self.assertEqual(move.state, 'posted')

    def test_negative_quantity_blocked(self):
        shareholder = self._create_shareholder()
        share_class = self._create_share_class()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                self._create_movement(
                    shareholder_id=shareholder.id,
                    share_class_id=share_class.id,
                    movement_type='issue',
                    quantity=-5)

    def test_transfer_requires_from_to(self):
        """Test that transfer requires both from and to shareholders."""
        share_class = self._create_share_class()
        holder1 = self._create_shareholder()
        # Missing to_shareholder_id
        with self.assertRaises(ValidationError):
            self._create_movement(
                from_shareholder_id=holder1.id,
                share_class_id=share_class.id,
                movement_type='transfer')
        # Missing from_shareholder_id
        with self.assertRaises(ValidationError):
            self._create_movement(
                to_shareholder_id=holder1.id,
                share_class_id=share_class.id,
                movement_type='transfer')

    def test_transfer_blocked_when_from_eq_to(self):
        """Test that transfer from and to same shareholder is blocked."""
        share_class = self._create_share_class()
        holder1 = self._create_shareholder()
        with self.cr.savepoint():
            with self.assertRaises(Exception):  # SQL constraint
                self._create_movement(
                    from_shareholder_id=holder1.id,
                    to_shareholder_id=holder1.id,
                    share_class_id=share_class.id,
                    movement_type='transfer')

    def test_transfer_allowed_when_sufficient(self):
        share_class = self._create_share_class()
        holder1 = self._create_shareholder()
        holder2 = self._create_shareholder(name='Holder Two')
        buy = self._create_movement(
            shareholder_id=holder1.id,
            share_class_id=share_class.id,
            quantity=50,
            movement_type='issue')
        buy.action_post()
        transfer = self._create_movement(
            from_shareholder_id=holder1.id,
            to_shareholder_id=holder2.id,
            share_class_id=share_class.id,
            quantity=20,
            movement_type='transfer')
        transfer.action_post()
        self.assertEqual(transfer.state, 'posted')
        self.assertEqual(holder1.total_shares, 30)
        self.assertEqual(holder2.total_shares, 20)

    def test_transfer_blocked_when_insufficient(self):
        share_class = self._create_share_class()
        holder1 = self._create_shareholder()
        holder2 = self._create_shareholder(name='Holder Two')
        transfer = self._create_movement(
            from_shareholder_id=holder1.id,
            to_shareholder_id=holder2.id,
            share_class_id=share_class.id,
            quantity=10,
            movement_type='transfer')
        with self.assertRaises(ValidationError):
            transfer.action_post()

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({
            'name': 'Capital Co 2'})
        shareholder2 = self.env['sf.shareholder'].with_company(company2).create({
            'name': 'Co2 Holder',
            'shareholder_type': 'individual',
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
        move = self._create_movement(
            shareholder_id=shareholder.id,
            share_class_id=share_class.id,
            movement_type='issue')
        move.action_post()
        cap_action = self.env.ref(
            'sf_corporate_capital.action_report_cap_table').report_action(
            shareholder)
        self.assertTrue(cap_action)
        cert_action = self.env.ref(
            'sf_corporate_capital.action_report_share_certificate').report_action(
            shareholder)
        self.assertTrue(cert_action)

    def test_authorized_shares_default_zero(self):
        share_class = self._create_share_class(authorized_shares=False)
        self.assertEqual(share_class.authorized_shares, 0)

    def test_shareholder_type_field(self):
        holder_ind = self._create_shareholder(shareholder_type='individual')
        holder_comp = self._create_shareholder(shareholder_type='company')
        self.assertEqual(holder_ind.shareholder_type, 'individual')
        self.assertEqual(holder_comp.shareholder_type, 'company')

    def test_issue_requires_shareholder(self):
        share_class = self._create_share_class()
        with self.assertRaises(ValidationError):
            self._create_movement(
                share_class_id=share_class.id,
                movement_type='issue')

    def test_buyback_requires_shareholder(self):
        share_class = self._create_share_class()
        with self.assertRaises(ValidationError):
            self._create_movement(
                share_class_id=share_class.id,
                movement_type='buyback')

    def test_transfer_forbids_shareholder_field(self):
        share_class = self._create_share_class()
        holder1 = self._create_shareholder()
        holder2 = self._create_shareholder(name='Holder Two')
        with self.assertRaises(ValidationError):
            self._create_movement(
                shareholder_id=holder1.id,
                from_shareholder_id=holder1.id,
                to_shareholder_id=holder2.id,
                share_class_id=share_class.id,
                movement_type='transfer')