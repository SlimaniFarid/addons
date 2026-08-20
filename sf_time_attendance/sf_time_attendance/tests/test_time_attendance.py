# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase


class TestTimeAttendance(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Shift = self.env['sf.time.attendance.shift']
        self.Monthly = self.env['sf.time.attendance.monthly']
        self.Employee = self.env['hr.employee']
        self.employee = self.Employee.create({'name': 'Jane Doe'})

    def test_01_shift_creation(self):
        shift = self.Shift.create({
            'employee_id': self.employee.id,
            'day_of_week': '0',
            'start_time': 9.0,
            'end_time': 17.0,
            'lunch_break_hours': 1.0,
        })
        self.assertEqual(shift.employee_id, self.employee)
        self.assertEqual(shift.day_of_week, '0')

    def test_02_shift_unique_per_weekday(self):
        self.Shift.create({
            'employee_id': self.employee.id, 'day_of_week': '1',
            'start_time': 9.0, 'end_time': 17.0,
        })
        with self.assertRaises(Exception):
            self.Shift.create({
                'employee_id': self.employee.id, 'day_of_week': '1',
                'start_time': 8.0, 'end_time': 16.0,
            })

    def test_03_expected_hours(self):
        shift = self.Shift.create({
            'employee_id': self.employee.id, 'day_of_week': '0',
            'start_time': 9.0, 'end_time': 17.0, 'lunch_break_hours': 1.0,
        })
        self.assertEqual(shift.expected_hours(), 7.0)

    def test_04_expected_hours_no_lunch(self):
        shift = self.Shift.create({
            'employee_id': self.employee.id, 'day_of_week': '1',
            'start_time': 8.0, 'end_time': 16.0, 'lunch_break_hours': 0.0,
        })
        self.assertEqual(shift.expected_hours(), 8.0)

    def test_05_monthly_summary(self):
        rec = self.Monthly.create({
            'employee_id': self.employee.id,
            'month': '2026-01-01',
        })
        self.assertEqual(rec.employee_id, self.employee)
        self.assertEqual(rec.worked_hours, 0.0)

    def test_06_monthly_unique_ok(self):
        rec1 = self.Monthly.create({
            'employee_id': self.employee.id, 'month': '2026-02-01',
        })
        rec2 = self.Monthly.create({
            'employee_id': self.employee.id, 'month': '2026-03-01',
        })
        self.assertNotEqual(rec1.id, rec2.id)

    def test_07_generate_all_monthly(self):
        # no attendance -> nothing generated
        self.Monthly.action_generate_all_monthly()
        self.assertEqual(self.Monthly.search_count([]), 0)

    def test_08_monthly_required_employee(self):
        with self.assertRaises(Exception):
            self.Monthly.create({'month': '2026-04-01'})