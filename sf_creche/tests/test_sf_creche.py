# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfCreche(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Child = self.env['sf.creche.child']
        self.Enrollment = self.env['sf.creche.enrollment']
        self.Attendance = self.env['sf.creche.attendance']
        self.Room = self.env['sf.creche.room']
        self.Billing = self.env['sf.creche.billing']
        self.group_user = self.env.ref('sf_creche.group_sf_creche_user')
        self.group_manager = self.env.ref(
            'sf_creche.group_sf_creche_manager')
        self.user = self.env['res.users'].create({
            'name': 'Creche User',
            'login': 'creche_user',
            'groups_id': [(4, self.group_user.id)],
        })

    def _create_child(self):
        return self.Child.create({
            'firstname': 'Emma',
            'lastname': 'Smith',
            'dob': '2022-03-10',
        })

    def _create_room(self, capacity=10):
        return self.Room.create({'capacity': capacity})

    def _create_enrollment(self, child=None, room=None):
        return self.Enrollment.create({
            'child_id': (child or self._create_child()).id,
            'room_id': (room or self._create_room()).id,
            'enrollment_date': '2026-01-01',
            'monthly_fee': 400.0,
        })

    def _create_done_attendance(self, child, date, arrival, departure):
        att = self.Attendance.create({
            'child_id': child.id,
            'date': date,
            'arrival_time': arrival,
            'departure_time': departure,
        })
        att.action_done()
        return att

    def test_create_records_with_sequences(self):
        child = self._create_child()
        self.assertTrue(child.name.startswith('CHD-'))
        room = self._create_room()
        self.assertTrue(room.name.startswith('ROM-'))
        enrollment = self._create_enrollment(child=child, room=room)
        self.assertTrue(enrollment.name.startswith('ENR-'))
        attendance = self.Attendance.create({
            'child_id': child.id,
            'date': '2026-08-05',
        })
        self.assertTrue(attendance.name.startswith('ATT-'))
        billing = self.Billing.create({
            'child_id': child.id,
            'month': '2026-08',
        })
        self.assertTrue(billing.name.startswith('BIL-'))

    def test_attendance_hours_computation(self):
        child = self._create_child()
        attendance = self.Attendance.create({
            'child_id': child.id,
            'date': '2026-08-05',
            'arrival_time': 8.0,
            'departure_time': 17.0,
        })
        self.assertEqual(attendance.hours, 9.0)
        attendance.write({'departure_time': False})
        self.assertEqual(attendance.hours, 0.0)
        attendance.write({
            'arrival_time': 9.0,
            'departure_time': 12.5,
        })
        self.assertEqual(attendance.hours, 3.5)

    def test_capacity_check_raises_user_error(self):
        room = self._create_room(capacity=1)
        child_a = self._create_child()
        child_b = self._create_child()
        enrollment_a = self._create_enrollment(child=child_a, room=room)
        enrollment_a.action_activate()
        enrollment_b = self._create_enrollment(child=child_b, room=room)
        enrollment_b.action_activate()
        self._create_done_attendance(child_a, '2026-08-05', 8.0, 12.0)
        attendance_b = self.Attendance.create({
            'child_id': child_b.id,
            'date': '2026-08-05',
            'arrival_time': 8.0,
            'departure_time': 12.0,
        })
        with self.assertRaises(UserError):
            attendance_b.action_done()
        self.assertEqual(attendance_b.state, 'draft')

    def test_billing_amount_computation(self):
        child = self._create_child()
        self.env.company.sf_creche_hourly_rate = 4.0
        self._create_done_attendance(child, '2026-08-03', 8.0, 17.0)
        self._create_done_attendance(child, '2026-08-04', 9.0, 12.0)
        billing = self.Billing.create({
            'child_id': child.id,
            'month': '2026-08',
        })
        self.assertEqual(billing.hours, 12.0)
        self.assertEqual(billing.hourly_rate, 4.0)
        self.assertEqual(billing.amount, 48.0)

    def test_enrollment_workflow_manager_only(self):
        enrollment = self._create_enrollment()
        with self.assertRaises(UserError):
            enrollment.with_user(self.user).action_activate()
        self.assertEqual(enrollment.state, 'draft')
        enrollment.action_activate()
        self.assertEqual(enrollment.state, 'active')
        with self.assertRaises(UserError):
            enrollment.with_user(self.user).action_end()
        self.assertEqual(enrollment.state, 'active')
        enrollment.action_end()
        self.assertEqual(enrollment.state, 'ended')

    def test_billing_workflow_manager_only(self):
        child = self._create_child()
        billing = self.Billing.create({
            'child_id': child.id,
            'month': '2026-08',
        })
        with self.assertRaises(UserError):
            billing.with_user(self.user).action_issue()
        self.assertEqual(billing.state, 'draft')
        billing.action_issue()
        self.assertEqual(billing.state, 'issued')
        with self.assertRaises(UserError):
            billing.with_user(self.user).action_pay()
        self.assertEqual(billing.state, 'issued')
        billing.action_pay()
        self.assertEqual(billing.state, 'paid')

    def test_cron_reminder_dedup(self):
        enrollment = self._create_enrollment()
        enrollment.action_activate()
        enrollment.end_date = fields.Date.today() + timedelta(days=5)
        self.env.company.sf_creche_alert_days = 14
        self.Enrollment._cron_enrollment_end_reminder()
        self.assertTrue(enrollment.activity_ids)
        count = len(enrollment.activity_ids)
        self.Enrollment._cron_enrollment_end_reminder()
        self.assertEqual(len(enrollment.activity_ids), count)

    def test_cron_reminder_ignores_far_end_date(self):
        enrollment = self._create_enrollment()
        enrollment.action_activate()
        enrollment.end_date = fields.Date.today() + timedelta(days=60)
        self.env.company.sf_creche_alert_days = 14
        self.Enrollment._cron_enrollment_end_reminder()
        self.assertFalse(enrollment.activity_ids)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({
            'name': 'Creche Company B',
        })
        other = self.Child.with_company(company_b).create({
            'firstname': 'Jane',
            'lastname': 'Doe',
        })
        self.assertNotIn(other, self.Child.with_user(self.user).search(
            [('id', '=', other.id)]))

    def test_reports_render(self):
        child = self._create_child()
        room = self._create_room(capacity=20)
        enrollment = self._create_enrollment(child=child, room=room)
        enrollment.action_activate()
        attendance = self._create_done_attendance(
            child, '2026-08-05', 8.0, 17.0)
        billing = self.Billing.create({
            'child_id': child.id,
            'month': '2026-08',
        })
        billing_report = self.env.ref('sf_creche.report_sf_creche_billing')
        self.assertEqual(billing_report.report_type, 'qweb-pdf')
        self.assertEqual(billing_report.model, 'sf.creche.billing')
        pdf, _format = billing_report._render_qweb_pdf([billing.id])
        self.assertTrue(pdf)
        attendance_report = self.env.ref(
            'sf_creche.report_sf_creche_attendance')
        self.assertEqual(attendance_report.report_type, 'qweb-pdf')
        self.assertEqual(attendance_report.model, 'sf.creche.attendance')
        pdf2, _format2 = attendance_report._render_qweb_pdf(
            [attendance.id])
        self.assertTrue(pdf2)
