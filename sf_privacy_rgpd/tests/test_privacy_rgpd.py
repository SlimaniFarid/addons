# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestPrivacyRgpd(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Treatment = self.env['sf.privacy.treatment']
        self.Assessment = self.env['sf.privacy.impact.assessment']
        self.Breach = self.env['sf.privacy.breach']
        self.Request = self.env['sf.privacy.request']
        self.group_user = self.env.ref('sf_privacy_rgpd.group_privacy_user')
        self.group_manager = self.env.ref(
            'sf_privacy_rgpd.group_privacy_manager')

    def _create_treatment(self):
        return self.Treatment.create({
            'title': 'HR Payroll Processing',
            'legal_basis': 'legal',
        })

    def _create_assessment(self, treatment=None):
        return self.Assessment.create({
            'treatment_id': (treatment or self._create_treatment()).id,
            'likelihood': 'medium',
            'severity': 'high',
        })

    def _create_manager(self):
        return self.env['res.users'].create({
            'name': 'Privacy Manager',
            'login': 'privacy_manager',
            'groups_id': [(4, self.group_manager.id)],
        })

    def _create_user(self):
        return self.env['res.users'].create({
            'name': 'Privacy User',
            'login': 'privacy_user',
            'groups_id': [(4, self.group_user.id)],
        })

    def test_create_treatment_with_sequence(self):
        treatment = self._create_treatment()
        self.assertTrue(treatment.name.startswith('PRT-'))

    def test_create_aipd_with_sequence(self):
        assessment = self._create_assessment()
        self.assertTrue(assessment.name.startswith('AIP-'))

    def test_create_breach_with_sequence(self):
        breach = self.Breach.create({'description': 'Lost laptop'})
        self.assertTrue(breach.name.startswith('BRH-'))

    def test_create_request_with_sequence(self):
        request = self.Request.create({
            'request_type': 'access',
            'person_name': 'John Doe',
        })
        self.assertTrue(request.name.startswith('REQ-'))

    def test_treatment_workflow(self):
        treatment = self._create_treatment()
        treatment.action_activate()
        self.assertEqual(treatment.state, 'active')
        treatment.action_start_review()
        self.assertEqual(treatment.state, 'under_review')
        self.assertTrue(treatment.last_review_date)
        treatment.action_close()
        self.assertEqual(treatment.state, 'closed')
        self.assertFalse(treatment.active)

    def test_next_review_date(self):
        treatment = self._create_treatment()
        treatment.write({'last_review_date': fields.Date.today(),
                         'review_frequency': 365})
        self.assertEqual(
            treatment.next_review_date,
            fields.Date.today() + timedelta(days=365))

    def test_aipd_risk_score(self):
        assessment = self._create_assessment()
        self.assertEqual(assessment.risk_score, 6)
        assessment.likelihood = 'high'
        assessment.severity = 'high'
        self.assertEqual(assessment.risk_score, 9)

    def test_aipd_manager_validation(self):
        assessment = self._create_assessment()
        manager = self._create_manager()
        assessment.action_submit()
        assessment.with_user(manager).action_start_review()
        assessment.with_user(manager).action_approve()
        self.assertEqual(assessment.state, 'approved')

    def test_aipd_rejection(self):
        assessment = self._create_assessment()
        manager = self._create_manager()
        assessment.action_submit()
        assessment.with_user(manager).action_start_review()
        assessment.with_user(manager).action_reject()
        self.assertEqual(assessment.state, 'rejected')

    def test_aipd_user_cannot_validate(self):
        assessment = self._create_assessment()
        user = self._create_user()
        assessment.action_submit()
        with self.assertRaises(UserError):
            assessment.with_user(user).action_start_review()

    def test_breach_workflow(self):
        breach = self.Breach.create({'description': 'Email leak'})
        breach.action_detect()
        self.assertEqual(breach.state, 'detected')
        self.assertTrue(breach.date_detected)
        breach.action_declare()
        self.assertEqual(breach.state, 'declared')
        self.assertEqual(breach.notification_status, 'reported')
        self.assertTrue(breach.notification_date)
        breach.measures = 'Rotate credentials'
        breach.action_remediate()
        self.assertEqual(breach.state, 'remediated')
        breach.action_close()
        self.assertEqual(breach.state, 'closed')

    def test_breach_close_requires_measures(self):
        breach = self.Breach.create({'description': 'Stolen device'})
        breach.action_detect()
        breach.action_declare()
        breach.action_remediate()
        with self.assertRaises(UserError):
            breach.action_close()

    def test_request_workflow(self):
        request = self.Request.create({
            'request_type': 'erasure',
            'person_name': 'Jane Doe',
        })
        request.action_start()
        self.assertEqual(request.state, 'in_progress')
        request.action_done()
        self.assertEqual(request.state, 'done')
        self.assertTrue(request.response_date)
        request.action_close()
        self.assertEqual(request.state, 'closed')

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create(
            {'name': 'Privacy Company B'})
        user = self._create_user()
        self._create_treatment()
        other = self.Treatment.with_company(company_b).create({
            'title': 'Marketing Data',
            'legal_basis': 'consent',
        })
        self.assertNotIn(other, self.Treatment.with_user(user).search(
            [('id', '=', other.id)]))

    def test_cron_review_alerts(self):
        treatment = self._create_treatment()
        treatment.write({
            'last_review_date': fields.Date.today() - timedelta(days=400),
            'review_frequency': 365,
        })
        treatment.action_activate()
        responsible = self._create_manager()
        treatment.responsible_id = responsible
        breach = self.Breach.create({'description': 'Data exposure'})
        breach.action_detect()
        breach.write({'date_detected': fields.Datetime.now()
                      - timedelta(hours=100)})
        self.Treatment._check_privacy_reviews()
        self.assertTrue(treatment.activity_ids)
        self.assertTrue(breach.activity_ids)