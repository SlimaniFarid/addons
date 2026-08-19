# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import UserError
from odoo import fields


class TestHseIncident(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Incident = self.env['sf.hse.incident']
        self.Action = self.env['sf.hse.incident.action']
        self.Risk = self.env['sf.hse.risk']
        self.Permit = self.env['sf.hse.permit']
        self.Ppe = self.env['sf.hse.ppe']
        self.Inspection = self.env['sf.hse.inspection']
        self.Checklist = self.env['sf.hse.inspection.checklist']
        self.employee = self.env['hr.employee'].create({
            'name': 'Test Employee',
        })
        self.manager = self.env['res.users'].create({
            'name': 'Manager',
            'login': 'hse_manager_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_hse_management.group_hse_manager').id,
                ]),
            ],
        })
        self.user = self.env['res.users'].create({
            'name': 'User',
            'login': 'hse_user_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_hse_management.group_hse_user').id,
                ]),
            ],
        })
        self.responsible = self.env['res.users'].create({
            'name': 'Responsible',
            'login': 'hse_resp_test',
        })

    def _make_incident(self, **kw):
        vals = {
            'incident_type': 'near_miss',
            'incident_date': fields.Datetime.now(),
            'severity': 'major',
            'description': 'Test near miss',
            'employee_id': self.employee.id,
        }
        vals.update(kw)
        return self.Incident.create(vals)

    def test_01_incident_workflow(self):
        incident = self._make_incident()
        self.assertEqual(incident.state, 'draft')
        incident.action_report()
        self.assertEqual(incident.state, 'reported')
        incident.action_start_investigation()
        self.assertEqual(incident.state, 'under_investigation')
        incident.action_resolve()
        self.assertEqual(incident.state, 'resolved')
        incident.action_close()
        self.assertEqual(incident.state, 'closed')

    def test_02_resolve_requires_closed_actions(self):
        incident = self._make_incident()
        incident.action_report()
        incident.action_start_investigation()
        self.Action.create({
            'incident_id': incident.id,
            'description': 'Fix guard',
            'responsible_id': self.responsible.id,
            'due_date': fields.Date.today(),
        })
        with self.assertRaises(UserError):
            incident.action_resolve()

    def test_03_action_done_requires_note(self):
        incident = self._make_incident()
        action = self.Action.create({
            'incident_id': incident.id,
            'description': 'Fix guard',
            'responsible_id': self.responsible.id,
            'due_date': fields.Date.today(),
        })
        with self.assertRaises(UserError):
            action.action_done()
        action.completion_note = 'Guard replaced'
        action.action_done()
        self.assertEqual(action.state, 'done')

    def test_04_risk_matrix(self):
        risk = self.Risk.create({
            'name': 'Working at height',
            'probability': 4,
            'severity': 5,
        })
        self.assertEqual(risk.risk_level, 20)
        self.assertEqual(risk.risk_class, 'extreme')

    def test_05_risk_out_of_bounds(self):
        with self.assertRaises(UserError):
            self.Risk.create({
                'name': 'Bad risk',
                'probability': 6,
                'severity': 2,
            })

    def test_06_permit_requires_manager(self):
        permit = self.Permit.create({
            'permit_type': 'fire',
            'employee_id': self.employee.id,
            'location': 'Workshop',
            'start_date': fields.Datetime.now(),
            'end_date': fields.Datetime.now(),
        })
        permit.action_submit()
        with self.assertRaises(UserError):
            permit.with_user(self.user).action_approve()
        permit.with_user(self.manager).action_approve()
        self.assertEqual(permit.state, 'approved')

    def test_07_permit_bad_dates(self):
        with self.assertRaises(UserError):
            self.Permit.create({
                'permit_type': 'fire',
                'employee_id': self.employee.id,
                'location': 'Workshop',
                'start_date': fields.Datetime.now(),
                'end_date': fields.Datetime.from_string('2020-01-01 00:00:00'),
            })

    def test_08_ppe_state(self):
        ppe = self.Ppe.create({
            'name': 'Helmet H1',
            'ppe_type': 'helmet',
            'expiry_date': fields.Date.from_string('2020-01-01'),
        })
        self.assertEqual(ppe.state, 'expired')
        ppe2 = self.Ppe.create({
            'name': 'Gloves G1',
            'ppe_type': 'gloves',
        })
        ppe2.employee_id = self.employee.id
        self.assertEqual(ppe2.state, 'assigned')

    def test_09_inspection_nonconformity(self):
        checklist = self.Checklist.create({
            'name': 'Fire Safety Check',
        })
        checklist.item_ids = [
            (0, 0, {'sequence': 1, 'name': 'Fire extinguisher present'}),
            (0, 0, {'sequence': 2, 'name': 'Exit clear'}),
        ]
        inspection = self.Inspection.create({
            'inspection_date': fields.Date.today(),
            'checklist_id': checklist.id,
        })
        self.assertEqual(len(inspection.items), 2)
        inspection.items[0].result = 'no'
        self.assertTrue(inspection.items[0].is_nonconformity)

    def test_10_incident_not_deletable_when_active(self):
        incident = self._make_incident()
        incident.action_report()
        with self.assertRaises(UserError):
            incident.unlink()