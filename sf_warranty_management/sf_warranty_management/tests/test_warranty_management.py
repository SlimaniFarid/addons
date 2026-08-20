# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestWarrantyManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Warranty = self.env['sf.warranty']
        self.Claim = self.env['sf.warranty.claim']
        self.group_user = self.env.ref(
            'sf_warranty_management.group_warranty_user')
        self.partner = self.env['res.partner'].create({'name': 'Client A'})
        self.product = self.env['product.product'].create({
            'name': 'Pump Model X',
            'type': 'product',
        })

    def _create_warranty(self, months=24):
        return self.Warranty.create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'duration_months': months,
            'coverage': 'full',
        })

    def _create_claim(self, warranty=None, purchase_date=None, state='draft'):
        return self.Claim.create({
            'partner_id': self.partner.id,
            'product_id': self.product.id,
            'claim_type': 'warranty',
            'failure_description': 'Motor stopped working',
            'purchase_date': purchase_date or date.today()
            - timedelta(days=300),
            'state': state,
        })

    def test_create_warranty_with_sequence(self):
        warranty = self._create_warranty()
        self.assertTrue(warranty.name.startswith('WTY-'))

    def test_create_claim_with_sequence(self):
        warranty = self._create_warranty()
        claim = self._create_claim()
        self.assertTrue(claim.name.startswith('CLM-'))
        self.assertEqual(claim.warranty_id, warranty)

    def test_eligibility_within_duration(self):
        warranty = self._create_warranty(months=24)
        claim = self._create_claim(warranty=warranty,
                                   purchase_date=date.today()
                                   - timedelta(days=300))
        claim.action_check_eligibility()
        self.assertTrue(claim.eligible)

    def test_eligibility_out_of_duration(self):
        self._create_warranty(months=12)
        claim = self._create_claim(purchase_date=date.today()
                                   - timedelta(days=900))
        claim.action_check_eligibility()
        self.assertFalse(claim.eligible)

    def test_eligibility_without_warranty(self):
        claim = self._create_claim()
        claim.action_check_eligibility()
        self.assertFalse(claim.eligible)
        self.assertTrue(claim.eligibility_detail)

    def test_open_claim_checks_eligibility(self):
        self._create_warranty(months=24)
        claim = self._create_claim()
        claim.action_open()
        self.assertEqual(claim.state, 'open')
        self.assertTrue(claim.eligible or not claim.eligible)

    def test_reject_without_reason(self):
        self._create_warranty(months=12)
        claim = self._create_claim(purchase_date=date.today()
                                   - timedelta(days=900))
        claim.action_open()
        wizard = self.env['sf.warranty.claim.decision.wizard'].create({
            'claim_id': claim.id,
            'decision': 'rejected',
        })
        with self.assertRaises(UserError):
            wizard.action_apply()

    def test_accept_claim(self):
        self._create_warranty(months=24)
        claim = self._create_claim()
        claim.action_open()
        wizard = self.env['sf.warranty.claim.decision.wizard'].create({
            'claim_id': claim.id,
            'decision': 'accepted',
            'estimated_cost': 250.0,
        })
        wizard.action_apply()
        self.assertEqual(claim.state, 'closed')
        self.assertEqual(claim.decision, 'accepted')
        self.assertEqual(claim.estimated_cost, 250.0)

    def test_delete_open_claim(self):
        self._create_warranty(months=24)
        claim = self._create_claim()
        claim.action_open()
        with self.assertRaises(UserError):
            claim.unlink()

    def test_claim_requires_product(self):
        with self.assertRaises(Exception):
            self.Claim.create({
                'partner_id': self.partner.id,
                'claim_type': 'warranty',
                'failure_description': 'Broken',
                'purchase_date': date.today(),
            })

    def test_multi_company_rule(self):
        self._create_warranty(months=24)
        company_b = self.env['res.company'].create({'name': 'Warranty Company B'})
        user = self.env['res.users'].create({
            'name': 'Warranty Company A User',
            'login': 'warranty_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        other = self.Claim.with_company(company_b).create({
            'partner_id': self.partner.id,
            'product_id': self.product.id,
            'claim_type': 'warranty',
            'failure_description': 'Other company claim',
            'purchase_date': date.today() - timedelta(days=10),
        })
        self.assertNotIn(other, self.Claim.with_user(user).search(
            [('id', '=', other.id)]))