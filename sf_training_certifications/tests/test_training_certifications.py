# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError


class TestTrainingCertifications(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Training = self.env['sf.training']
        self.Session = self.env['sf.training.session']
        self.Registration = self.env['sf.training.registration']
        self.Certification = self.env['sf.employee.certification']
        self.Matrix = self.env['sf.compliance.matrix']
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
        })
        self.category = self.env['sf.training.category'].create({
            'name': 'HSE',
            'code': 'HSE',
        })
        self.training = self.Training.create({
            'name': 'First Aid',
            'category_id': self.category.id,
            'duration_hours': 8.0,
            'mandatory': True,
        })
        self.session = self.Session.create({
            'training_id': self.training.id,
            'date_start': '2026-01-01 09:00:00',
            'date_end': '2026-01-01 17:00:00',
        })
        self.registration = self.Registration.create({
            'session_id': self.session.id,
            'employee_id': self.employee.id,
        })

    def _make_active_cert(self, issue, expiration=False):
        self.session.action_plan()
        self.session.action_done()
        cert = self.Certification.create({
            'employee_id': self.employee.id,
            'training_id': self.training.id,
            'registration_id': self.registration.id,
            'certificate_number': 'CERT-001',
            'issue_date': issue,
            'expiration_date': expiration,
            'state': 'active',
        })
        return cert

    def test_01_training_creation(self):
        self.assertEqual(self.training.name, 'First Aid')
        self.assertTrue(self.training.mandatory)
        self.assertTrue(self.training.active)

    def test_02_session_workflow(self):
        self.assertEqual(self.session.state, 'draft')
        self.session.action_plan()
        self.assertEqual(self.session.state, 'planned')
        self.session.action_done()
        self.assertEqual(self.session.state, 'done')
        self.assertEqual(self.session.attendee_count, 1)

    def test_03_plan_requires_registrations(self):
        empty = self.Session.create({
            'training_id': self.training.id,
            'date_start': '2026-02-01 09:00:00',
            'date_end': '2026-02-01 17:00:00',
        })
        with self.assertRaises(UserError):
            empty.action_plan()

    def test_04_certify_non_done_session_blocked(self):
        self.session.action_plan()
        wizard = self.env['sf.certification.issue.wizard'].create({
            'session_id': self.session.id,
            'issue_date': '2026-01-15',
        })
        with self.assertRaises(UserError):
            wizard.action_issue()

    def test_05_issue_certificates_for_done_session(self):
        self.session.action_plan()
        self.session.action_done()
        wizard = self.env['sf.certification.issue.wizard'].create({
            'session_id': self.session.id,
            'issue_date': '2026-01-15',
            'expiration_date': '2027-01-15',
        })
        wizard.action_issue()
        certs = self.Certification.search([
            ('employee_id', '=', self.employee.id),
        ])
        self.assertEqual(len(certs), 1)
        self.assertEqual(certs[0].state, 'active')
        self.assertEqual(certs[0].expiration_date,
                         certs[0].issue_date.replace(
                             year=certs[0].issue_date.year + 1))

    def test_06_expiration_before_issue_rejected(self):
        with self.assertRaises(UserError):
            self.Certification.create({
                'employee_id': self.employee.id,
                'training_id': self.training.id,
                'certificate_number': 'CERT-X',
                'issue_date': '2026-01-15',
                'expiration_date': '2025-12-31',
            })

    def test_07_duplicate_certificate_rejected(self):
        self._make_active_cert('2026-01-15')
        with self.assertRaises(Exception):
            self.Certification.create({
                'employee_id': self.employee.id,
                'training_id': self.training.id,
                'certificate_number': 'CERT-001',
                'issue_date': '2026-02-01',
            })

    def test_08_expiration_cron(self):
        from datetime import date, timedelta
        today = date.today()
        cert = self._make_active_cert(
            today.isoformat(),
            (today + timedelta(days=15)).isoformat())
        self.Certification._cron_check_expiration()
        self.assertEqual(cert.state, 'expiring')

    def test_09_no_expiration_stays_active(self):
        cert = self._make_active_cert('2026-01-15')
        self.Certification._cron_check_expiration()
        self.assertEqual(cert.state, 'active')

    def test_10_expired_certification(self):
        from datetime import date, timedelta
        today = date.today()
        cert = self._make_active_cert(
            (today - timedelta(days=400)).isoformat(),
            (today - timedelta(days=30)).isoformat())
        self.Certification._cron_check_expiration()
        self.assertEqual(cert.state, 'expired')

    def test_11_renewal_creates_new_cert(self):
        from datetime import date, timedelta
        today = date.today()
        cert = self._make_active_cert(
            today.isoformat(),
            (today + timedelta(days=15)).isoformat())
        self.Certification._cron_check_expiration()
        self.assertEqual(cert.state, 'expiring')
        wizard = self.env['sf.certification.renew.wizard'].create({
            'certification_id': cert.id,
            'new_issue_date': today.isoformat(),
            'new_expiration_date':
                (today + timedelta(days=365)).isoformat(),
        })
        new = wizard.action_renew()
        new_cert = self.env['sf.employee.certification'].browse(new['res_id'])
        self.assertEqual(cert.state, 'renewed')
        self.assertEqual(new_cert.state, 'active')
        self.assertEqual(new_cert.employee_id.id, self.employee.id)

    def test_12_compliance_matrix_refresh(self):
        self.Matrix._refresh_matrix()
        rows = self.Matrix.search([
            ('employee_id', '=', self.employee.id),
            ('training_id', '=', self.training.id),
        ])
        self.assertTrue(rows)
        self.assertFalse(rows[0].compliant)

    def test_13_compliance_matrix_compliant_after_cert(self):
        self._make_active_cert('2026-01-15')
        self.Matrix._refresh_matrix()
        row = self.Matrix.search([
            ('employee_id', '=', self.employee.id),
            ('training_id', '=', self.training.id),
        ])[0]
        self.assertTrue(row.compliant)