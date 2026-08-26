# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSchoolManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Year = self.env['sf.school.year']
        self.Group = self.env['sf.school.group']
        self.Teacher = self.env['sf.school.teacher']
        self.Student = self.env['sf.school.student']
        self.Course = self.env['sf.school.course']
        self.Enrollment = self.env['sf.school.enrollment']
        self.Grade = self.env['sf.school.grade']
        self.Absence = self.env['sf.school.absence']
        self.Tuition = self.env['sf.school.tuition']
        self.group_user = self.env.ref(
            'sf_school_management.group_school_user')

    def _create_year(self):
        return self.Year.create({})

    def _create_group(self, year=None):
        return self.Group.create({
            'year_id': (year or self._create_year()).id,
            'level': 'Grade 6',
        })

    def _create_teacher(self):
        return self.Teacher.create({
            'email': 'teacher@school.example',
        })

    def _create_student(self, group=None):
        student = self.Student.create({
            'group_id': (group or self._create_group()).id,
            'birth_date': '2014-03-10',
        })
        student.action_activate()
        return student

    def _create_course(self, subject='Mathematics', teacher=None):
        return self.Course.create({
            'subject': subject,
            'teacher_id': (teacher or self._create_teacher()).id,
        })

    def test_create_records_with_sequences(self):
        year = self._create_year()
        self.assertTrue(year.name.startswith('SCY-'))
        group = self._create_group(year=year)
        self.assertTrue(group.name.startswith('GRP-'))
        teacher = self._create_teacher()
        self.assertTrue(teacher.name.startswith('TEA-'))
        student = self.Student.create({'group_id': group.id})
        self.assertTrue(student.name.startswith('STU-'))
        course = self._create_course(teacher=teacher)
        self.assertTrue(course.name.startswith('COU-'))
        enrollment = self.Enrollment.create({
            'student_id': student.id,
            'course_id': course.id,
            'year_id': year.id,
        })
        self.assertTrue(enrollment.name.startswith('ENR-'))
        grade = self.Grade.create({
            'student_id': student.id,
            'course_id': course.id,
            'period': 'S1',
            'grade': 15.0,
        })
        self.assertTrue(grade.name.startswith('GRA-'))
        absence = self.Absence.create({
            'student_id': student.id,
            'course_id': course.id,
            'reason': 'illness',
        })
        self.assertTrue(absence.name.startswith('ABS-'))
        tuition = self.Tuition.create({
            'student_id': student.id,
            'year_id': year.id,
            'amount': 500.0,
        })
        self.assertTrue(tuition.name.startswith('TUI-'))

    def test_weighted_average(self):
        year = self._create_year()
        group = self._create_group(year=year)
        student = self._create_student(group=group)
        teacher = self._create_teacher()
        course_a = self._create_course(subject='Mathematics', teacher=teacher)
        course_b = self._create_course(subject='Physics', teacher=teacher)
        self.Grade.create({
            'student_id': student.id,
            'course_id': course_a.id,
            'period': 'S1',
            'grade': 14.0,
            'coefficient': 2.0,
        }).action_confirm()
        self.Grade.create({
            'student_id': student.id,
            'course_id': course_a.id,
            'period': 'S2',
            'grade': 10.0,
            'coefficient': 1.0,
        }).action_confirm()
        self.Grade.create({
            'student_id': student.id,
            'course_id': course_b.id,
            'period': 'S1',
            'grade': 12.0,
            'coefficient': 3.0,
        }).action_confirm()
        self.assertEqual(student.get_weighted_average(), 12.33)
        averages = student.get_subject_averages()
        by_subject = {entry['subject']: entry['average']
                      for entry in averages}
        self.assertEqual(by_subject['Mathematics'], 12.67)
        self.assertEqual(by_subject['Physics'], 12.0)

    def test_tuition_paid_and_overdue_alert(self):
        year = self._create_year()
        group = self._create_group(year=year)
        student = self._create_student(group=group)
        paid = self.Tuition.create({
            'student_id': student.id,
            'year_id': year.id,
            'amount': 500.0,
            'paid_amount': 500.0,
        })
        self.assertEqual(paid.state, 'paid')
        overdue = self.Tuition.create({
            'student_id': student.id,
            'year_id': year.id,
            'amount': 400.0,
            'due_date': fields.Date.today() - timedelta(days=30),
        })
        self.assertEqual(overdue.state, 'overdue')
        overdue._check_school_alerts()
        self.assertTrue(overdue.activity_ids)

    def test_grade_confirmation_manager_only(self):
        year = self._create_year()
        group = self._create_group(year=year)
        student = self._create_student(group=group)
        course = self._create_course()
        grade = self.Grade.create({
            'student_id': student.id,
            'course_id': course.id,
            'period': 'S1',
            'grade': 16.0,
        })
        user = self.env['res.users'].create({
            'name': 'School Teacher',
            'login': 'school_teacher_user',
            'groups_id': [(4, self.group_user.id)],
        })
        with self.assertRaises(UserError):
            grade.with_user(user).action_confirm()
        self.assertEqual(grade.state, 'draft')
        grade.action_confirm()
        self.assertEqual(grade.state, 'confirmed')

    def test_absence_workflow(self):
        year = self._create_year()
        group = self._create_group(year=year)
        student = self._create_student(group=group)
        course = self._create_course()
        justified = self.Absence.create({
            'student_id': student.id,
            'course_id': course.id,
            'reason': 'illness',
        })
        justified.action_set_justified()
        self.assertEqual(justified.state, 'justified')
        self.assertTrue(justified.justified)
        unjustified = self.Absence.create({
            'student_id': student.id,
            'course_id': course.id,
            'reason': 'other',
        })
        unjustified.action_set_unjustified()
        self.assertEqual(unjustified.state, 'unjustified')
        self.assertFalse(unjustified.justified)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({
            'name': 'School Company B',
        })
        user = self.env['res.users'].create({
            'name': 'School Company A User',
            'login': 'school_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        year = self._create_year()
        group = self._create_group(year=year)
        other = self.Student.with_company(company_b).create({
            'group_id': group.id,
        })
        self.assertNotIn(other, self.Student.with_user(user).search(
            [('id', '=', other.id)]))

    def test_report_records_exist(self):
        report_card = self.env.ref(
            'sf_school_management.report_school_report_card')
        self.assertEqual(report_card.report_type, 'qweb-pdf')
        self.assertEqual(report_card.model, 'sf.school.student')
        report_fees = self.env.ref(
            'sf_school_management.report_school_unpaid_fees')
        self.assertEqual(report_fees.report_type, 'qweb-pdf')
        self.assertEqual(report_fees.model, 'sf.school.tuition')