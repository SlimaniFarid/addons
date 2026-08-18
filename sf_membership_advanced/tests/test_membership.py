from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
from datetime import date, timedelta

class TestMembership(TransactionCase):

    def setUp(self):
        super().setUp()
        self.plan = self.env['membership.plan'].create({
            'name': 'Test Plan',
            'code': 'TEST',
            'fee': 100.0,
            'duration_months': 12,
        })
        self.partner = self.env['res.partner'].create({
            'name': 'Test Member',
            'email': 'test@example.com',
        })
        self.member = self.env['membership.member'].create({
            'partner_id': self.partner.id,
        })

    def test_plan_creation(self):
        self.assertEqual(self.plan.fee, 100.0)
        self.assertTrue(self.plan.active)

    def test_member_creation(self):
        self.assertEqual(self.member.partner_id, self.partner)
        self.assertEqual(self.member.status, 'pending')
        self.assertTrue(self.member.member_code.startswith('MEM-'))

    def test_subscription_lifecycle(self):
        sub = self.env['membership.subscription'].create({
            'member_id': self.member.id,
            'plan_id': self.plan.id,
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=365),
            'amount': 100.0,
        })
        self.assertEqual(sub.state, 'draft')
        sub.action_activate()
        self.assertEqual(sub.state, 'active')
        self.member.invalidate_recordset()
        self.assertEqual(self.member.status, 'active')

    def test_payment_activates_subscription(self):
        sub = self.env['membership.subscription'].create({
            'member_id': self.member.id,
            'plan_id': self.plan.id,
            'start_date': date.today(),
            'end_date': date.today() + timedelta(days=365),
            'amount': 100.0,
        })
        pay = self.env['membership.payment'].create({
            'member_id': self.member.id,
            'subscription_id': sub.id,
            'amount': 100.0,
        })
        pay.action_confirm()
        self.assertEqual(pay.state, 'paid')
        sub.invalidate_recordset()
        self.assertEqual(sub.state, 'active')

    def test_negative_fee_rejected(self):
        with self.assertRaises(ValidationError):
            self.env['membership.plan'].create({
                'name': 'Bad',
                'code': 'BAD',
                'fee': -10.0,
            })