# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.fields import Datetime


class TestMesShopFloor(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Station = self.env['sf.mes.station']
        self.WorkOrder = self.env['sf.mes.work.order']
        self.Downtime = self.env['sf.mes.downtime']
        self.QualityCheck = self.env['sf.mes.quality.check']
        self.station = self.Station.create({
            'name': 'CNC Mill', 'code': 'CNC-1'})
        self.product = self.env['product.product'].create({
            'name': 'Housing Part'})
        self.order = self.WorkOrder.create({
            'name': 'WO-001',
            'product_id': self.product.id,
            'quantity': 10.0,
            'station_id': self.station.id,
        })

    def test_01_station_creation(self):
        self.assertEqual(self.station.code, 'CNC-1')

    def test_02_station_code_unique(self):
        with self.assertRaises(Exception):
            self.Station.create({'name': 'Other', 'code': 'CNC-1'})

    def test_03_work_order_lifecycle(self):
        self.assertEqual(self.order.state, 'pending')
        self.order.action_start()
        self.assertEqual(self.order.state, 'running')
        self.assertTrue(self.order.started_at)
        self.order.action_pause()
        self.assertEqual(self.order.state, 'paused')
        self.order.action_resume()
        self.assertEqual(self.order.state, 'running')
        self.order.action_done()
        self.assertEqual(self.order.state, 'done')
        self.assertTrue(self.order.finished_at)
        self.assertEqual(self.order.units_produced, 10.0)

    def test_04_duration_computed(self):
        self.order.action_start()
        self.order.finished_at = Datetime.add(self.order.started_at,
                                              minutes=90)
        self.order._compute_duration()
        self.assertEqual(self.order.duration_minutes, 90)

    def test_05_downtime_minutes(self):
        dt = self.Downtime.create({
            'work_order_id': self.order.id,
            'station_id': self.station.id,
            'start': Datetime.now(),
            'end': Datetime.add(Datetime.now(), minutes=25),
            'reason': 'Tool change',
        })
        self.assertEqual(dt.minutes, 25)

    def test_06_quality_check(self):
        qc = self.QualityCheck.create({
            'work_order_id': self.order.id,
            'product_id': self.product.id,
            'check_type': 'dimensional',
            'result': 'pass',
        })
        self.assertEqual(qc.result, 'pass')
        self.assertEqual(len(self.order.quality_check_ids), 1)