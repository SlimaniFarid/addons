# -*- coding: utf-8 -*-
import uuid

from odoo import fields as odoo_fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfGiftsHospitality(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Counterparty %s' % uuid.uuid4().hex[:6],
        })
        self.user_group = self.env.ref(
            'sf_gifts_hospitality.group_sf_gifts_hospitality_user')
        self.manager_group = self.env.ref(
            'sf_gifts_hospitality.group_sf_gifts_hospitality_manager')

    def _create_gift(self, value=30.0, **kw):
        vals = {
            'direction': 'received',
            'counterparty_id': self.partner.id,
            'category': 'gift',
            'description': 'Business gift',
            'estimated_value': value,
        }
        vals.update(kw)
        return self.env['sf.gift.hospitality'].create(vals)

    def _create_user(self, group):
        return self.env['res.users'].create({
            'name': 'Gift User',
            'login': 'gift_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [group.id])],
        })

    def test_sequence(self):
        gift = self._create_gift()
        self.assertTrue(gift.name.startswith('GFT-'))

    def test_below_threshold_auto_approved(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'sf_gifts_hospitality.approval_threshold', '50.0')
        gift = self._create_gift(value=30.0)
        self.assertFalse(gift.requires_approval)
        gift.action_submit()
        self.assertEqual(gift.state, 'approved')
        self.assertTrue(gift.approved_date)

    def test_above_threshold_requires_approval(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'sf_gifts_hospitality.approval_threshold', '50.0')
        gift = self._create_gift(value=100.0)
        self.assertTrue(gift.requires_approval)
        gift.action_submit()
        self.assertEqual(gift.state, 'submitted')

    def test_approve_reject_manager_only(self):
        gift = self._create_gift(value=100.0)
        gift.action_submit()
        user = self._create_user(self.user_group)
        with self.assertRaises(UserError):
            gift.with_user(user).action_approve()
        manager = self._create_user(self.manager_group)
        gift.with_user(manager).action_approve()
        self.assertEqual(gift.state, 'approved')

    def test_resubmit_after_reject(self):
        gift = self._create_gift(value=100.0)
        gift.action_submit()
        manager = self._create_user(self.manager_group)
        gift.with_user(manager).action_reject()
        self.assertEqual(gift.state, 'rejected')
        gift.action_resubmit()
        self.assertEqual(gift.state, 'submitted')

    def test_state_write_guard(self):
        gift = self._create_gift()
        with self.assertRaises(UserError):
            gift.write({'state': 'approved'})

    def test_value_immutable_after_approval(self):
        gift = self._create_gift(value=30.0)
        gift.action_submit()
        with self.assertRaises(UserError):
            gift.write({'estimated_value': 5.0})

    def test_archive_manager_only(self):
        gift = self._create_gift(value=30.0)
        gift.action_submit()
        user = self._create_user(self.user_group)
        with self.assertRaises(UserError):
            gift.with_user(user).action_archive()

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({
            'name': 'Gift Co 2'})
        gift2 = self.env['sf.gift.hospitality'].with_company(company2).create({
            'direction': 'given',
            'category': 'meal',
            'description': 'Client meal',
            'estimated_value': 40.0,
            'company_id': company2.id,
        })
        user = self._create_user(self.user_group)
        user.write({
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.gift.hospitality'].with_user(user).search(
            [('id', '=', gift2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        gift = self._create_gift()
        gift.action_submit()
        for report in ['action_report_gift_register',
                       'action_report_gift_declaration']:
            action = self.env.ref(
                'sf_gifts_hospitality.%s' % report).report_action(gift)
            self.assertTrue(action)

    def test_declaration_lines(self):
        today = odoo_fields.Date.today()
        g1 = self._create_gift(value=20.0)
        g2 = self._create_gift(value=30.0)
        lines = (g1 | g2)._declaration_lines()
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]['total'], 50.0)
        self.assertEqual(today.year, lines[0]['year'])