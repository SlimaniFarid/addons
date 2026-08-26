# -*- coding: utf-8 -*-
from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.tests import TransactionCase, tagged
from odoo import fields


@tagged('post_install', '-at_install')
class TestOccupationalHealth(TransactionCase):

    def setUp(self):
        super().setUp()
        self.File = self.env['sf.oh.medical.file']
        self.Visit = self.env['sf.oh.visit']
        self.Employee = self.env['hr.employee']
        self.group_manager = self.env.ref(
            'sf_occupational_health.group_oh_manager')
        self.group_user = self.env.ref(
            'sf_occupational_health.group_oh_user')

    def _create_employee(self, name='Employee A'):
        return self.Employee.create({'name': name})

    def _create_file(self, employee):
        return self.File.create({'employee_id': employee.id})

    def test_create_file(self):
        employee = self._create_employee()
        file = self._create_file(employee)
        self.assertEqual(file.state, 'active')

    def test_unique_file_per_employee(self):
        employee = self._create_employee()
        self._create_file(employee)
        with self.assertRaises(Exception):
            self._create_file(employee)

    def test_visit_workflow_and_aptitude(self):
        employee = self._create_employee()
        file = self._create_file(employee)
        visit = self.Visit.create({
            'medical_file_id': file.id,
            'visit_type': 'hire',
        })
        visit.action_plan()
        self.assertEqual(visit.state, 'planned')
        wizard = self.env['sf.oh.schedule.wizard'].create({
            'visit_id': visit.id,
            'doctor_id': self.env['sf.oh.doctor'].create(
                {'name': 'Dr Test'}).id,
            'planned_date': fields.Date.today(),
        })
        wizard.action_confirm()
        self.assertEqual(visit.state, 'scheduled')
        result = self.env['sf.oh.visit.result.wizard'].create({
            'visit_id': visit.id,
            'result': 'inapt',
            'restriction_note': 'No heavy lifting',
            'validity_from': fields.Date.today(),
            'validity_to': fields.Date.today(),
        })
        result.action_confirm()
        self.assertEqual(visit.state, 'done')
        self.assertEqual(file.last_aptitude, 'inapt')
        self.assertEqual(file.last_visit_date, fields.Date.today())

    def test_done_requires_result(self):
        employee = self._create_employee()
        file = self._create_file(employee)
        visit = self.Visit.create({
            'medical_file_id': file.id,
            'visit_type': 'hire',
        })
        with self.assertRaises(ValidationError):
            visit.write({'state': 'done'})

    def test_invalid_validity_period(self):
        employee = self._create_employee()
        file = self._create_file(employee)
        visit = self.Visit.create({
            'medical_file_id': file.id,
            'visit_type': 'hire',
            'validity_from': fields.Date.today(),
            'validity_to': fields.Date.today(),
        })
        with self.assertRaises(ValidationError):
            visit.write({'validity_to': fields.Date(2020, 1, 1)})

    def test_next_due_date_from_upcoming_visit(self):
        employee = self._create_employee()
        file = self._create_file(employee)
        due = fields.Date.today()
        self.Visit.create({
            'medical_file_id': file.id,
            'visit_type': 'periodic',
            'state': 'planned',
            'planned_date': due,
        })
        self.assertEqual(file.next_due_date, due)

    def test_cron_alert_and_auto_create(self):
        self.env['res.users'].create({
            'name': 'OH Manager',
            'login': 'oh_manager_user',
            'groups_id': [(6, 0, [self.group_user.id,
                                  self.group_manager.id])],
        })
        employee = self._create_employee()
        file = self._create_file(employee)
        due = fields.Date.today() + fields.timedelta(days=20)
        self.Visit.create({
            'medical_file_id': file.id,
            'visit_type': 'hire',
            'state': 'done',
            'result': 'apt',
            'done_date': fields.Date.today(),
            'validity_from': fields.Date.today(),
            'validity_to': due,
        })
        self.env.company.sf_oh_alert_days = 30
        self.env.company.sf_oh_auto_create_periodic = True
        file._check_oh_expiry_alerts()
        self.assertTrue(
            file.visit_ids.filtered(lambda v: v.visit_type == 'periodic'))
        self.assertTrue(file.activity_ids)

    def test_restriction_access_denied_to_user(self):
        user = self.env['res.users'].create({
            'name': 'OH Plain User',
            'login': 'oh_plain_user',
            'groups_id': [(4, self.group_user.id)],
        })
        employee = self._create_employee()
        file = self._create_file(employee)
        restriction = self.env['sf.oh.restriction'].create({
            'medical_file_id': file.id,
            'name': 'No heavy lifting',
        })
        with self.assertRaises(AccessError):
            self.env['sf.oh.restriction'].with_user(user).browse(
                restriction.id).read(['name'])

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'OH Company B'})
        user = self.env['res.users'].create({
            'name': 'OH Company A User',
            'login': 'oh_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        employee = self.env['hr.employee'].with_company(company_b).create(
            {'name': 'Employee B'})
        other = self.File.with_company(company_b).create(
            {'employee_id': employee.id})
        self.assertNotIn(other, self.File.with_user(user).search(
            [('id', '=', other.id)]))

    def test_close_requires_no_open_visits(self):
        employee = self._create_employee()
        file = self._create_file(employee)
        self.Visit.create({
            'medical_file_id': file.id,
            'visit_type': 'hire',
        })
        with self.assertRaises(UserError):
            file.action_close()

    def test_active_file_cannot_be_deleted(self):
        employee = self._create_employee()
        file = self._create_file(employee)
        with self.assertRaises(UserError):
            file.unlink()