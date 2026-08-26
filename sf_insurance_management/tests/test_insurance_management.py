# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestInsuranceManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Company = self.env['sf.insurance.company']
        self.Policy = self.env['sf.insurance.policy']
        self.Claim = self.env['sf.insurance.claim']
        self.group_user = self.env.ref(
            'sf_insurance_management.group_insurance_user')
        self.group_manager = self.env.ref(
            'sf_insurance_management.group_insurance_manager')
        self.env.user.groups_id += self.group_manager

    def _create_insurer(self):
        return self.Company.create({'reference': 'REF-001', 'rating': 'A'})

    def _create_policy(self, **kw):
        vals = {
            'insurer_id': self._create_insurer().id,
            'policy_type': 'liability',
            'start_date': fields.Date.today() - timedelta(days=30),
            'end_date': fields.Date.today() + timedelta(days=335),
            'premium_amount': 1200.0,
            'premium_frequency': 'annual',
            'state': 'active',
        }
        vals.update(kw)
        return self.Policy.create(vals)

    def _create_claim(self, policy=None, **kw):
        vals = {
            'policy_id': (policy or self._create_policy()).id,
            'date_occurred': fields.Date.today() - timedelta(days=3),
            'date_notified': fields.Date.today() - timedelta(days=2),
            'description': 'Damage reported on site',
        }
        vals.update(kw)
        return self.Claim.create(vals)

    def _declare_review_estimate(self, claim):
        claim.action_declare()
        claim.action_review()
        claim.action_estimate()
        return claim

    def test_create_insurer_policy_guarantee_claim(self):
        insurer = self._create_insurer()
        self.assertTrue(insurer.name.startswith('INS-'))
        policy = self._create_policy()
        self.assertTrue(policy.name.startswith('POL-'))
        self.assertTrue(policy.policy_number)
        policy.write({'guarantee_ids': [(0, 0, {
            'name': 'RC Guarantee',
            'guarantee_type': 'Third party liability',
            'coverage_amount': 1000000.0,
            'deductible': 500.0,
        })]})
        self.assertEqual(len(policy.guarantee_ids), 1)
        claim = self._create_claim(policy=policy)
        self.assertTrue(claim.name.startswith('CLA-'))
        self.assertTrue(claim.claim_number)

    def test_policy_expiry_and_claim_reminder(self):
        policy = self._create_policy(
            end_date=fields.Date.today() - timedelta(days=5))
        claim = self._create_claim(policy=policy,
                                   date_occurred=fields.Date.today()
                                   - timedelta(days=10),
                                   date_notified=False)
        self.Policy._check_policies()
        self.assertEqual(policy.state, 'expired')
        self.assertTrue(claim.activity_ids)

    def test_policy_renewal_reminder(self):
        self.env.company.sf_insurance_remind_days = 30
        policy = self._create_policy(
            end_date=fields.Date.today() + timedelta(days=5))
        self.Policy._check_policies()
        self.assertEqual(policy.state, 'active')
        self.assertTrue(policy.activity_ids)

    def test_auto_renewal_creates_new_period(self):
        old_end = fields.Date.today() - timedelta(days=5)
        policy = self._create_policy(end_date=old_end, auto_renew=True)
        self.Policy._check_policies()
        self.assertEqual(policy.state, 'expired')
        new_policy = self.Policy.search([
            ('id', '!=', policy.id),
            ('policy_number', '=', policy.policy_number),
            ('state', '=', 'active'),
        ])
        self.assertTrue(new_policy)
        self.assertEqual(new_policy.start_date, old_end)
        self.assertEqual(new_policy.end_date,
                         old_end + timedelta(days=365))
        self.assertEqual(new_policy.policy_number, policy.policy_number)

    def test_claim_settled_requires_amount(self):
        claim = self._create_claim(estimated_amount=1000.0)
        self._declare_review_estimate(claim)
        with self.assertRaises(UserError):
            claim.action_settle()

    def test_claim_rejected_requires_note(self):
        claim = self._create_claim(estimated_amount=1000.0)
        claim.action_declare()
        with self.assertRaises(UserError):
            claim.action_reject()

    def test_claim_settled_ok(self):
        claim = self._create_claim(estimated_amount=1000.0)
        self._declare_review_estimate(claim)
        claim.settlement_amount = 900.0
        claim.action_settle()
        self.assertEqual(claim.state, 'settled')
        self.assertTrue(claim.closed_date)

    def test_claim_rejected_requires_note_ok(self):
        claim = self._create_claim(estimated_amount=1000.0)
        self._declare_review_estimate(claim)
        claim.notes = 'Not covered by the policy'
        claim.action_reject()
        self.assertEqual(claim.state, 'rejected')

    def test_settle_reject_manager_only(self):
        user = self.env['res.users'].create({
            'name': 'Insurance Company User',
            'login': 'insurance_company_user',
            'company_id': self.env.company.id,
            'groups_id': [(4, self.group_user.id)],
        })
        claim = self._create_claim(estimated_amount=1000.0)
        self._declare_review_estimate(claim)
        with self.assertRaises(UserError):
            claim.with_user(user).action_settle()
        claim2 = self._create_claim(estimated_amount=1000.0)
        claim2.action_declare()
        claim2.notes = 'Not covered'
        with self.assertRaises(UserError):
            claim2.with_user(user).action_reject()

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({
            'name': 'Insurance Company B'})
        user = self.env['res.users'].create({
            'name': 'Insurance Company A User',
            'login': 'insurance_company_a_user',
            'company_id': self.env.company.id,
            'groups_id': [(4, self.group_user.id)],
        })
        other = self._create_policy()
        other.with_company(company_b).company_id = company_b.id
        self.assertNotIn(other, self.Policy.with_user(user).search(
            [('id', '=', other.id)]))

    def test_reports_exist(self):
        program = self.env.ref(
            'sf_insurance_management.report_insurance_program')
        self.assertEqual(program.model, 'sf.insurance.policy')
        self.assertEqual(
            program.report_name,
            'sf_insurance_management.insurance_program_template')
        claims = self.env.ref(
            'sf_insurance_management.report_insurance_claims')
        self.assertEqual(claims.model, 'sf.insurance.claim')
        self.assertEqual(
            claims.report_name,
            'sf_insurance_management.claims_report_template')