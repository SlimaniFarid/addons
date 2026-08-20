# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields


class TestOnboarding(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Template = self.env['sf.onboarding.template']
        self.Program = self.env['sf.onboarding.program']
        self.Task = self.env['sf.onboarding.task']
        self.Wizard = self.env['sf.onboarding.generate.wizard']
        self.manager = self.env['res.users'].create({
            'name': 'Manager',
            'login': 'onboarding_manager_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref(
                        'sf_hr_onboarding.group_onboarding_manager').id,
                ]),
            ],
        })
        self.user = self.env['res.users'].create({
            'name': 'User',
            'login': 'onboarding_user_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref(
                        'sf_hr_onboarding.group_onboarding_user').id,
                ]),
            ],
        })
        self.responsible = self.env['res.users'].create({
            'name': 'Responsible',
            'login': 'onboarding_resp_test',
        })
        self.template = self.Template.create({
            'name': 'Standard Onboarding',
            'program_type': 'onboarding',
        })
        self.template.task_ids = [
            (0, 0, {
                'sequence': 1,
                'name': 'Create email account',
                'responsible_type': 'it',
                'required': True,
            }),
            (0, 0, {
                'sequence': 2,
                'name': 'Prepare laptop',
                'responsible_type': 'it',
                'required': True,
            }),
            (0, 0, {
                'sequence': 3,
                'name': 'Welcome coffee',
                'responsible_type': 'hr',
                'required': False,
            }),
        ]

    def _make_employee(self):
        employee = self.env['hr.employee'].create({
            'name': 'New Employee',
        })
        return employee

    def test_01_auto_generate_on_employee_creation(self):
        employee = self._make_employee()
        program = self.Program.search([
            ('employee_id', '=', employee.id),
            ('program_type', '=', 'onboarding'),
        ], limit=1)
        self.assertTrue(program)
        self.assertEqual(program.state, 'in_progress')
        self.assertEqual(len(program.task_ids), 3)

    def test_02_progress_calculation(self):
        employee = self._make_employee()
        program = self.Program.search([
            ('employee_id', '=', employee.id),
        ], limit=1)
        self.assertEqual(program.progress, 0.0)
        required = program.task_ids.filtered(lambda t: t.required)
        required[0].action_mark_done()
        self.assertEqual(program.progress, 50.0)
        required[1].action_mark_done()
        self.assertEqual(program.progress, 100.0)

    def test_03_complete_requires_required_tasks(self):
        employee = self._make_employee()
        program = self.Program.search([
            ('employee_id', '=', employee.id),
        ], limit=1)
        with self.assertRaises(UserError):
            program.action_complete()
        for task in program.task_ids.filtered(lambda t: t.required):
            task.action_mark_done()
        program.action_complete()
        self.assertEqual(program.state, 'completed')

    def test_04_wizard_generation_offboarding(self):
        employee = self._make_employee()
        offboard = self.Template.create({
            'name': 'Standard Offboarding',
            'program_type': 'offboarding',
        })
        offboard.task_ids = [(0, 0, {
            'sequence': 1,
            'name': 'Return laptop',
            'required': True,
        })]
        wizard = self.Wizard.create({
            'employee_id': employee.id,
            'program_type': 'offboarding',
            'template_id': offboard.id,
            'key_date': fields.Date.today(),
        })
        wizard.action_generate()
        program = self.Program.search([
            ('employee_id', '=', employee.id),
            ('program_type', '=', 'offboarding'),
        ], limit=1)
        self.assertTrue(program)
        self.assertEqual(program.state, 'in_progress')

    def test_05_wizard_requires_template(self):
        employee = self._make_employee()
        wizard = self.Wizard.create({
            'employee_id': employee.id,
            'program_type': 'offboarding',
            'key_date': fields.Date.today(),
        })
        with self.assertRaises(UserError):
            wizard.action_generate()

    def test_06_skip_optional_task(self):
        employee = self._make_employee()
        program = self.Program.search([
            ('employee_id', '=', employee.id),
        ], limit=1)
        optional = program.task_ids.filtered(lambda t: not t.required)
        optional.action_skip()
        self.assertEqual(optional.state, 'skipped')

    def test_07_program_not_deletable_in_progress(self):
        employee = self._make_employee()
        program = self.Program.search([
            ('employee_id', '=', employee.id),
        ], limit=1)
        with self.assertRaises(UserError):
            program.unlink()

    def test_08_late_task_activity(self):
        employee = self._make_employee()
        program = self.Program.search([
            ('employee_id', '=', employee.id),
        ], limit=1)
        task = program.task_ids.filtered(lambda t: t.required)[0]
        task.responsible_id = self.responsible
        task.due_date = fields.Date.from_string('2020-01-01')
        self.Task._check_late_tasks()
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'sf.onboarding.task'),
            ('res_id', '=', task.id),
        ])
        self.assertTrue(activities)

    def test_09_single_active_onboarding(self):
        employee = self._make_employee()
        employee._auto_generate_onboarding()
        programs = self.Program.search([
            ('employee_id', '=', employee.id),
            ('program_type', '=', 'onboarding'),
            ('state', 'in', ('draft', 'in_progress')),
        ])
        self.assertEqual(len(programs), 1)