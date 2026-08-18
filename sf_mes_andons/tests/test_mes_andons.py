# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.fields import Datetime


class TestMesAndons(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Station = self.env['sf.andon.station']
        self.Call = self.env['sf.andon.call']
        self.Rule = self.env['sf.andon.escalation.rule']
        self.Log = self.env['sf.andon.response.log']

        self.station = self.Station.create({
            'name': 'Assembly Line 1', 'code': 'ASM-01',
            'location': 'Building A, Floor 1',
        })
        self.work_order = self.env['sf.mes.work.order'].create({
            'name': 'WO-001',
            'product_id': self.env['product.product'].create({'name': 'Widget'}).id,
            'quantity': 100.0,
            'station_id': self.env['sf.mes.station'].create({'name': 'Station 1', 'code': 'ST-1'}).id,
        })

    def test_01_station_creation(self):
        self.assertEqual(self.station.code, 'ASM-01')
        self.assertEqual(self.station.open_calls_count, 0)

    def test_02_station_code_unique(self):
        with self.assertRaises(Exception):
            self.Station.create({'name': 'Other', 'code': 'ASM-01'})

    def test_03_call_creation(self):
        call = self.Call.create({
            'station_id': self.station.id,
            'call_type': 'quality',
            'severity': 'high',
            'description': 'Defect detected',
        })
        self.assertEqual(call.state, 'new')
        self.assertEqual(call.priority, 90)  # high(80) + quality(10)
        self.assertEqual(self.station.open_calls_count, 1)

    def test_04_priority_computation(self):
        call_critical = self.Call.create({
            'station_id': self.station.id, 'call_type': 'safety', 'severity': 'critical',
        })
        self.assertEqual(call_critical.priority, 120)  # critical(100) + safety(20)

        call_low = self.Call.create({
            'station_id': self.station.id, 'call_type': 'material', 'severity': 'low',
        })
        self.assertEqual(call_low.priority, 15)  # low(10) + material(5)

    def test_05_call_lifecycle(self):
        call = self.Call.create({
            'station_id': self.station.id, 'call_type': 'maintenance', 'severity': 'medium',
        })
        call.action_acknowledge()
        self.assertEqual(call.state, 'acknowledged')
        self.assertTrue(call.acknowledged_date)
        self.assertEqual(call.assigned_user_id, self.env.user)

        call.action_start_work()
        self.assertEqual(call.state, 'in_progress')

        call.action_resolve()
        self.assertEqual(call.state, 'resolved')
        self.assertTrue(call.resolved_date)

        call.action_close()
        self.assertEqual(call.state, 'closed')
        self.assertTrue(call.closed_date)

    def test_06_response_time_computed(self):
        call = self.Call.create({
            'station_id': self.station.id, 'call_type': 'quality', 'severity': 'high',
        })
        call.acknowledged_date = Datetime.add(call.create_date, minutes=7)
        call.resolved_date = Datetime.add(call.create_date, minutes=45)
        call._compute_times()
        self.assertAlmostEqual(call.response_time, 7.0, places=1)
        self.assertAlmostEqual(call.resolution_time, 45.0, places=1)

    def test_07_escalation_rule(self):
        rule = self.Rule.create({
            'name': 'Quality L1', 'call_type': 'quality', 'level': 1,
            'trigger_delay': 5, 'send_email': True,
        })
        self.assertEqual(rule.level, 1)
        self.assertEqual(rule.call_type, 'quality')

    def test_08_escalation_unique(self):
        self.Rule.create({'name': 'Q1', 'call_type': 'quality', 'level': 1})
        with self.assertRaises(Exception):
            self.Rule.create({'name': 'Q1b', 'call_type': 'quality', 'level': 1})

    def test_09_response_log(self):
        call = self.Call.create({
            'station_id': self.station.id, 'call_type': 'quality', 'severity': 'high',
        })
        call.action_acknowledge()
        logs = self.Log.search([('call_id', '=', call.id)])
        self.assertTrue(logs)
        self.assertEqual(logs[0].action, 'acknowledged')