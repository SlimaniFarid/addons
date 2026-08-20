# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestBusinessContinuity(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Process = self.env['sf.bcp.process']
        self.Strategy = self.env['sf.bcp.strategy']
        self.Plan = self.env['sf.bcp.plan']
        self.Exercise = self.env['sf.bcp.exercise']
        self.group_user = self.env.ref(
            'sf_business_continuity.group_bcp_user')
        self.group_manager = self.env.ref(
            'sf_business_continuity.group_bcp_manager')
        self.env.user.groups_id += self.group_manager

    def _create_process(self, **kw):
        vals = {
            'department_id': 'IT',
            'criticality': 'critical',
            'rto': 4,
            'rpo': 1,
            'impact': 50000.0,
            'dependencies': 'ERP, network',
        }
        vals.update(kw)
        return self.Process.create(vals)

    def _create_plan(self, process=None, **kw):
        vals = {
            'process_id': (process or self._create_process()).id,
            'version': '1.0',
            'summary': '<p>Recovery summary</p>',
            'steps': '<p>Recovery steps</p>',
            'owner_id': self.env.user.partner_id.id,
            'resource_ids': 'Backup servers',
        }
        vals.update(kw)
        return self.Plan.create(vals)

    def test_create_records_with_sequences(self):
        process = self._create_process()
        self.assertTrue(process.name.startswith('BCP-'))
        strategy = self.Strategy.create({
            'process_id': process.id,
            'strategy_type': 'alternate_site',
            'detail': 'Cold site',
            'cost': 12000.0,
        })
        self.assertTrue(strategy.name.startswith('STR-'))
        plan = self._create_plan(process=process)
        self.assertTrue(plan.name.startswith('PLN-'))
        exercise = self.Exercise.create({
            'plan_id': plan.id,
            'exercise_date': fields.Date.today(),
            'scenario': 'Server room fire',
            'participants': 'IT team',
            'objectives': 'Restore within RTO',
        })
        self.assertTrue(exercise.name.startswith('EXE-'))

    def test_next_review_date_computation(self):
        self.env.company.sf_bcp_review_days = 365
        plan = self._create_plan()
        plan.action_publish()
        self.assertEqual(
            plan.next_review_date,
            fields.Date.today() + timedelta(days=365))
        plan.write({
            'published_date': fields.Date.today() - timedelta(days=400),
            'last_review_date': fields.Date.today(),
        })
        self.assertEqual(
            plan.next_review_date,
            fields.Date.today() + timedelta(days=365))

    def test_publish_requires_content(self):
        plan = self._create_plan(summary=False, steps=False)
        with self.assertRaises(UserError):
            plan.action_publish()
        plan.summary = '<p>Summary</p>'
        with self.assertRaises(UserError):
            plan.action_publish()
        plan.steps = '<p>Steps</p>'
        plan.action_publish()
        self.assertEqual(plan.state, 'published')
        self.assertTrue(plan.published_date)
        self.assertTrue(plan.last_review_date)

    def test_publish_manager_only(self):
        user = self.env['res.users'].create({
            'name': 'BCP Company User',
            'login': 'bcp_company_user',
            'company_id': self.env.company.id,
            'groups_id': [(4, self.group_user.id)],
        })
        plan = self._create_plan()
        with self.assertRaises(UserError):
            plan.with_user(user).action_publish()

    def test_bia_validation_manager_only(self):
        user = self.env['res.users'].create({
            'name': 'BCP Company User 2',
            'login': 'bcp_company_user_2',
            'company_id': self.env.company.id,
            'groups_id': [(4, self.group_user.id)],
        })
        process = self._create_process()
        process.action_assess()
        with self.assertRaises(UserError):
            process.with_user(user).action_validate()

    def test_exercise_done_requires_results(self):
        plan = self._create_plan()
        exercise = self.Exercise.create({
            'plan_id': plan.id,
            'exercise_date': fields.Date.today(),
            'scenario': 'Cyberattack drill',
            'objectives': 'Test the recovery plan',
        })
        exercise.action_execute()
        with self.assertRaises(UserError):
            exercise.action_done()
        exercise.results = '<p>Restored in 3 hours</p>'
        exercise.action_done()
        self.assertEqual(exercise.state, 'done')

    def test_cron_review_alerts(self):
        self.env.company.sf_bcp_review_days = 365
        plan = self._create_plan()
        plan.action_publish()
        plan.write({
            'published_date': fields.Date.today() - timedelta(days=400),
            'last_review_date': False,
        })
        self.Plan._check_bcp_reviews()
        self.assertTrue(plan.activity_ids)
        self.Plan._check_bcp_reviews()
        self.assertEqual(len(plan.activity_ids), 1)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({
            'name': 'Business Continuity Company B'})
        user = self.env['res.users'].create({
            'name': 'BCP Company A User',
            'login': 'bcp_company_a_user',
            'company_id': self.env.company.id,
            'groups_id': [(4, self.group_user.id)],
        })
        other = self._create_process()
        other.with_company(company_b).company_id = company_b.id
        self.assertNotIn(other, self.Process.with_user(user).search(
            [('id', '=', other.id)]))

    def test_reports_exist(self):
        bia = self.env.ref(
            'sf_business_continuity.report_bia')
        self.assertEqual(bia.model, 'sf.bcp.process')
        self.assertEqual(
            bia.report_name,
            'sf_business_continuity.report_bia_template')
        recovery = self.env.ref(
            'sf_business_continuity.report_recovery_plan')
        self.assertEqual(recovery.model, 'sf.bcp.plan')
        self.assertEqual(
            recovery.report_name,
            'sf_business_continuity.report_recovery_plan_template')