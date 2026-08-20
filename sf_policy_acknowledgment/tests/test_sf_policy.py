# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields as odoo_fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfPolicy(TransactionCase):

    def setUp(self):
        super().setUp()
        self.employee1 = self.env['hr.employee'].create({'name': 'Emp One'})
        self.employee2 = self.env['hr.employee'].create({'name': 'Emp Two'})
        self.user_group = self.env.ref(
            'sf_policy_acknowledgment.group_sf_policy_user')
        self.manager_group = self.env.ref(
            'sf_policy_acknowledgment.group_sf_policy_manager')
        self.todo = self.env.ref('mail.mail_activity_data_todo')

    def _create_policy(self, **kw):
        vals = {
            'policy_type': 'hr',
            'version': '1.0',
            'effective_date': odoo_fields.Date.today(),
            'owner_id': self.env.user.id,
            'body': '<p>Policy content.</p>',
            'employee_ids': [(6, 0, [self.employee1.id, self.employee2.id])],
        }
        vals.update(kw)
        return self.env['sf.policy'].create(vals)

    def _create_user(self, group):
        return self.env['res.users'].create({
            'name': 'Policy User',
            'login': 'policy_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [group.id])],
        })

    def test_sequences(self):
        policy = self._create_policy()
        self.assertTrue(policy.name.startswith('PLCY-'))
        policy.action_publish()
        ack = policy.acknowledgment_ids[0]
        self.assertTrue(ack.name.startswith('ACK-'))

    def test_publish_generates_acks(self):
        policy = self._create_policy()
        policy.action_publish()
        self.assertEqual(len(policy.acknowledgment_ids), 2)
        self.assertTrue(
            all(a.state == 'pending' for a in policy.acknowledgment_ids))

    def test_acknowledge(self):
        policy = self._create_policy()
        policy.action_publish()
        ack = policy.acknowledgment_ids[0]
        ack.action_acknowledge()
        self.assertEqual(ack.state, 'acknowledged')
        self.assertTrue(ack.acknowledged_date)
        self.assertEqual(ack.acknowledged_by, self.env.user)

    def test_acknowledgment_rate(self):
        policy = self._create_policy()
        policy.action_publish()
        policy.acknowledgment_ids[0].action_acknowledge()
        self.assertEqual(policy.acknowledgment_rate, 50.0)

    def test_unique_acknowledgment(self):
        policy = self._create_policy()
        with self.cr.savepoint():
            with self.assertRaises(Exception):
                self.env['sf.policy.acknowledgment'].create({
                    'policy_id': policy.id,
                    'employee_id': self.employee1.id,
                })

    def test_ack_requires_published(self):
        policy = self._create_policy()
        ack = self.env['sf.policy.acknowledgment'].create({
            'policy_id': policy.id,
            'employee_id': self.employee1.id,
        })
        with self.assertRaises(UserError):
            ack.action_acknowledge()

    def test_publish_manager_only(self):
        policy = self._create_policy()
        user = self._create_user(self.user_group)
        with self.assertRaises(UserError):
            policy.with_user(user).action_publish()

    def test_state_write_guard(self):
        policy = self._create_policy()
        with self.assertRaises(UserError):
            policy.write({'state': 'published'})

    def test_published_immutable(self):
        policy = self._create_policy()
        policy.action_publish()
        with self.assertRaises(UserError):
            policy.write({'body': '<p>Changed</p>'})

    def test_acknowledged_immutable(self):
        policy = self._create_policy()
        policy.action_publish()
        ack = policy.acknowledgment_ids[0]
        ack.action_acknowledge()
        with self.assertRaises(UserError):
            ack.write({'employee_id': self.employee2.id})

    def test_cron_ack_reminders(self):
        policy = self._create_policy()
        policy.action_publish()
        user1 = self._create_user(self.user_group)
        self.employee1.user_id = user1.id
        self.env['sf.policy.acknowledgment']._cron_ack_reminders()
        self.assertTrue(
            policy.acknowledgment_ids.filtered(
                lambda a: a.employee_id == self.employee1).activity_ids)
        policy.acknowledgment_ids[0].action_acknowledge()
        policy.acknowledgment_ids[1].action_acknowledge()
        self.env['sf.policy.acknowledgment']._cron_ack_reminders()
        self.assertFalse(
            policy.acknowledgment_ids.filtered(
                lambda a: a.activity_ids))

    def test_cron_expiry_reminders(self):
        today = odoo_fields.Date.today()
        policy = self._create_policy(
            expiry_date=today + timedelta(days=10))
        policy.action_publish()
        far = self._create_policy(
            name='Far Policy',
            expiry_date=today + timedelta(days=120))
        far.action_publish()
        self.env['sf.policy']._cron_expiry_reminders()
        self.assertTrue(policy.activity_ids)
        self.assertFalse(far.activity_ids)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({
            'name': 'Policy Co 2'})
        policy2 = self.env['sf.policy'].with_company(company2).create({
            'name': 'Co2 Policy',
            'policy_type': 'it',
            'effective_date': odoo_fields.Date.today(),
            'company_id': company2.id,
        })
        user = self._create_user(self.user_group)
        user.write({
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.policy'].with_user(user).search(
            [('id', '=', policy2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        policy = self._create_policy()
        policy.action_publish()
        ack = policy.acknowledgment_ids[0]
        ack.action_acknowledge()
        for report in ['action_report_policy',
                       'action_report_policy_acknowledgment']:
            action = self.env.ref(
                'sf_policy_acknowledgment.%s' % report).report_action(
                ack if report.endswith('acknowledgment') else policy)
            self.assertTrue(action)