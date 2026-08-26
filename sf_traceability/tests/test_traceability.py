# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestTraceability(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Recall = self.env['sf.traceability.recall']
        self.Lot = self.env['stock.lot']
        self.Product = self.env['product.product']
        self.product = self.Product.create({'name': 'Beverage', 'type': 'product'})
        self.lot = self.Lot.create({
            'name': 'B-2026-001',
            'product_id': self.product.id,
        })

    def test_01_lot_creation(self):
        self.assertEqual(self.lot.name, 'B-2026-001')
        self.assertEqual(self.lot.product_id, self.product)
        self.assertEqual(self.lot.quality_status, 'ok')

    def test_02_recall_creation(self):
        recall = self.Recall.create({
            'lot_id': self.lot.id,
            'severity': 'high',
        })
        self.assertEqual(recall.severity, 'high')
        self.assertEqual(recall.state, 'open')
        self.assertTrue(recall.name.startswith('RECALL/'))

    def test_03_recall_required_lot(self):
        with self.assertRaises(Exception):
            self.Recall.create({'severity': 'critical'})

    def test_04_recall_workflow(self):
        recall = self.Recall.create({'lot_id': self.lot.id})
        recall.action_start()
        self.assertEqual(recall.state, 'in_progress')
        recall.action_close()
        self.assertEqual(recall.state, 'closed')

    def test_05_lot_quality_blocked(self):
        self.lot.write({'quality_status': 'blocked'})
        self.assertEqual(self.lot.quality_status, 'blocked')

    def test_06_lot_expiry(self):
        self.lot.write({'expiry_date': '2026-12-31', 'batch_origin': 'Plant A'})
        self.assertEqual(self.lot.expiry_date, '2026-12-31')
        self.assertEqual(self.lot.batch_origin, 'Plant A')

    def test_07_recall_affected_zero(self):
        recall = self.Recall.create({'lot_id': self.lot.id})
        self.assertEqual(recall.move_count, 0)
        self.assertEqual(recall.partner_count, 0)

    def test_08_recall_links_to_lot(self):
        recall = self.Recall.create({'lot_id': self.lot.id})
        self.assertEqual(len(self.lot.recall_ids), 1)
        self.assertEqual(self.lot.recall_ids[0].id, recall.id)