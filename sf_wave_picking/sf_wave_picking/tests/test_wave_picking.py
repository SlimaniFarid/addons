# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestWavePicking(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Wave = self.env['sf.wave.picking']
        self.warehouse = self.env.ref('stock.warehouse0')
        self.ptype = self.env['stock.picking.type'].create({
            'name': 'Internal Test',
            'code': 'internal',
            'warehouse_id': self.warehouse.id,
            'sequence_code': 'INT-TEST',
        })

    def _make_picking(self):
        return self.env['stock.picking'].create({
            'picking_type_id': self.ptype.id,
            'location_id': self.warehouse.lot_stock_id.id,
            'location_dest_id': self.warehouse.lot_stock_id.id,
        })

    def test_01_wave_creation(self):
        wave = self.Wave.create({
            'name': 'WAVE-001',
            'warehouse_id': self.warehouse.id,
            'picking_type_id': self.ptype.id,
        })
        self.assertEqual(wave.state, 'draft')
        self.assertEqual(wave.move_count, 0)

    def test_02_wave_from_pickings(self):
        p1 = self._make_picking()
        p2 = self._make_picking()
        wave = self.Wave.create_wave_from_pickings(p1.ids + p2.ids)
        self.assertEqual(len(wave.picking_ids), 2)
        self.assertTrue(p1.sf_wave_id == wave)
        self.assertTrue(p2.sf_wave_id == wave)

    def test_03_wave_from_pickings_empty(self):
        wave = self.Wave.create_wave_from_pickings([])
        self.assertFalse(wave.picking_ids)

    def test_04_release_state(self):
        wave = self.Wave.create({
            'name': 'WAVE-002',
            'picking_type_id': self.ptype.id,
        })
        wave.action_release()
        self.assertEqual(wave.state, 'released')
        self.assertTrue(wave.date_start)

    def test_05_done_state(self):
        wave = self.Wave.create({'name': 'WAVE-003'})
        wave.action_done()
        self.assertEqual(wave.state, 'done')