# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta


class TestToolManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Tool = self.env['sf.tool']
        self.Category = self.env['sf.tool.category']
        self.Calibration = self.env['sf.tool.calibration']
        self.WearLog = self.env['sf.tool.wear.log']
        self.Assignment = self.env['sf.tool.assignment']
        self.category = self.Category.create({'name': 'End Mills'})
        self.tool = self.Tool.create({
            'code': 'EM-001',
            'name': 'Carbide End Mill 10mm',
            'tool_type': 'cutting',
            'category_id': self.category.id,
            'calibration_required': False,
            'max_wear': 100.0,
            'wear_unit': 'hours',
            'wear_alert_threshold': 80.0,
        })

    def test_01_tool_creation(self):
        self.assertEqual(self.tool.code, 'EM-001')
        self.assertEqual(self.tool.state, 'available')
        self.assertEqual(self.tool.current_wear, 0.0)
        self.assertEqual(self.tool.wear_status, 'good')

    def test_02_code_unique(self):
        with self.assertRaises(Exception):
            self.Tool.create({'code': 'EM-001', 'name': 'Other'})

    def test_03_assign_return(self):
        self.tool.action_assign()
        self.assertEqual(self.tool.state, 'assigned')
        self.assertEqual(self.tool.current_holder_id, self.env.user)
        self.tool.action_return()
        self.assertEqual(self.tool.state, 'available')
        self.assertFalse(self.tool.current_holder_id)

    def test_04_wear_tracking(self):
        self.tool.log_wear(10.0, 'hours')
        self.assertEqual(self.tool.current_wear, 10.0)
        self.tool.log_wear(20.0, 'hours')
        self.assertEqual(self.tool.current_wear, 30.0)
        logs = self.WearLog.search([('tool_id', '=', self.tool.id)])
        self.assertEqual(len(logs), 2)

    def test_05_wear_status(self):
        self.tool.write({'max_wear': 100.0, 'current_wear': 95.0, 'wear_alert_threshold': 80.0})
        self.assertEqual(self.tool.wear_status, 'warning')
        self.tool.write({'current_wear': 100.0})
        self.assertEqual(self.tool.wear_status, 'critical')
        self.tool.write({'current_wear': 50.0})
        self.assertEqual(self.tool.wear_status, 'good')

    def test_06_calibration_required(self):
        tool_cal = self.Tool.create({
            'code': 'GAGE-001',
            'name': 'Micrometer',
            'tool_type': 'measuring',
            'calibration_required': True,
            'calibration_frequency': 365,
        })
        tool_cal.write({'last_calibration_date': fields.Date.today() - timedelta(days=400)})
        self.assertEqual(tool_cal.calibration_status, 'overdue')
        tool_cal.write({'last_calibration_date': fields.Date.today() - timedelta(days=30)})
        self.assertEqual(tool_cal.calibration_status, 'due_soon')
        tool_cal.write({'last_calibration_date': fields.Date.today() - timedelta(days=100)})
        self.assertEqual(tool_cal.calibration_status, 'valid')

    def test_07_calibration_receive(self):
        tool_cal = self.Tool.create({
            'code': 'GAGE-002',
            'name': 'Caliper',
            'tool_type': 'measuring',
            'calibration_required': True,
        })
        tool_cal.action_send_calibration()
        self.assertEqual(tool_cal.state, 'calibration')
        tool_cal.action_receive_calibration()
        self.assertEqual(tool_cal.state, 'available')
        self.assertEqual(tool_cal.last_calibration_date, fields.Date.today())
        cals = self.Calibration.search([('tool_id', '=', tool_cal.id)])
        self.assertEqual(len(cals), 1)

    def test_08_calibration_not_required(self):
        self.tool.write({'calibration_required': False})
        self.assertEqual(self.tool.calibration_status, 'not_required')

    def test_09_assignment_log(self):
        self.tool.action_assign()
        assignment = self.Assignment.search([('tool_id', '=', self.tool.id), ('state', '=', 'assigned')])
        self.assertEqual(len(assignment), 1)
        self.assertEqual(assignment.user_id, self.env.user)

    def test_10_next_calibration_date(self):
        tool_cal = self.Tool.create({
            'code': 'GAGE-003',
            'name': 'Gauge Block',
            'tool_type': 'measuring',
            'calibration_required': True,
            'calibration_frequency': 180,
        })
        today = fields.Date.today()
        tool_cal.write({'last_calibration_date': today})
        self.assertEqual(tool_cal.next_calibration_date, today + timedelta(days=180))