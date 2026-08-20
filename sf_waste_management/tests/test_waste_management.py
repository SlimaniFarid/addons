# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestWasteManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Bsd = self.env['sf.waste.bsd']
        self.Site = self.env['sf.waste.site']
        self.Code = self.env['sf.waste.code']
        self.group_user = self.env.ref(
            'sf_waste_management.group_waste_user')
        self.site = self.Site.create({
            'name': 'Plant A',
            'site_code': 'PA-01',
        })
        self.code = self.Code.create({
            'name': 'METAL',
            'description': 'Metal scrap',
            'category': 'Industrial',
        })

    def _create_bsd(self, state='draft'):
        return self.Bsd.create({
            'site_id': self.site.id,
            'waste_code_id': self.code.id,
            'quantity_kg': 500.0,
            'state': state,
        })

    def test_create_bsd_with_sequence(self):
        bsd = self._create_bsd()
        self.assertTrue(bsd.name.startswith('BSD-'))

    def test_positive_quantity_constraint(self):
        with self.assertRaises(ValidationError):
            self.Bsd.create({
                'site_id': self.site.id,
                'waste_code_id': self.code.id,
                'quantity_kg': -1,
            })

    def test_emit_flow(self):
        bsd = self._create_bsd()
        bsd.action_emit()
        self.assertEqual(bsd.state, 'emitted')
        self.assertTrue(bsd.emit_date)

    def test_transfer_flow(self):
        bsd = self._create_bsd()
        bsd.action_emit()
        bsd.action_transfer()
        self.assertEqual(bsd.state, 'transferred')

    def test_receive_flow(self):
        bsd = self._create_bsd()
        bsd.action_emit()
        bsd.action_transfer()
        bsd.action_receive()
        self.assertEqual(bsd.state, 'received')
        self.assertTrue(bsd.reception_date)

    def test_archive_flow(self):
        bsd = self._create_bsd()
        bsd.action_emit()
        bsd.action_transfer()
        bsd.action_receive()
        bsd.action_archive()
        self.assertEqual(bsd.state, 'archived')

    def test_cancel_only_draft(self):
        bsd = self._create_bsd()
        bsd.action_emit()
        with self.assertRaises(UserError):
            bsd.action_cancel()

    def test_emit_only_draft(self):
        bsd = self._create_bsd()
        bsd.action_emit()
        with self.assertRaises(UserError):
            bsd.action_emit()

    def test_delete_emitted(self):
        bsd = self._create_bsd()
        bsd.action_emit()
        with self.assertRaises(UserError):
            bsd.unlink()

    def test_reception_date_before_emission(self):
        bsd = self._create_bsd()
        bsd.action_emit()
        bsd.action_transfer()
        with self.assertRaises(ValidationError):
            bsd.action_receive()
            bsd.reception_date = bsd.emit_date - timedelta(days=5)
            bsd._check_dates()

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Waste Company B'})
        user = self.env['res.users'].create({
            'name': 'Waste Company A User',
            'login': 'waste_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        site_b = self.Site.with_company(company_b).create({'name': 'Plant B'})
        bsd_b = self.Bsd.with_company(company_b).create({
            'site_id': site_b.id,
            'waste_code_id': self.code.id,
            'quantity_kg': 100.0,
        })
        self.assertNotIn(bsd_b, self.Bsd.with_user(user).search(
            [('id', '=', bsd_b.id)]))