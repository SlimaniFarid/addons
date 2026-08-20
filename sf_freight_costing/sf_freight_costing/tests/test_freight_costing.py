# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestFreightCosting(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Carrier = self.env['sf.freight.carrier']
        self.Cost = self.env['sf.freight.cost']
        self.fixed = self.Carrier.create({
            'name': 'Fixed Carrier', 'code': 'FIX', 'cost_method': 'fixed',
            'fixed_price': 50.0, 'min_charge': 20.0,
        })
        self.weight = self.Carrier.create({
            'name': 'Weight Carrier', 'code': 'WGT', 'cost_method': 'weight',
            'per_kg': 2.5, 'min_charge': 10.0,
        })
        self.value = self.Carrier.create({
            'name': 'Value Carrier', 'code': 'VAL', 'cost_method': 'value',
            'percent_value': 5.0, 'min_charge': 15.0,
        })

    def test_01_fixed_cost(self):
        total = self.Carrier.compute_cost(self.fixed, 0, 0, 0)
        self.assertEqual(total, 50.0)

    def test_02_fixed_min_charge(self):
        low = self.Carrier.create({
            'name': 'Low Fixed', 'cost_method': 'fixed',
            'fixed_price': 5.0, 'min_charge': 20.0,
        })
        self.assertEqual(self.Carrier.compute_cost(low, 0, 0, 0), 20.0)

    def test_03_weight_cost(self):
        total = self.Carrier.compute_cost(self.weight, 100, 0, 0)
        self.assertEqual(total, 250.0)

    def test_04_weight_min_charge(self):
        total = self.Carrier.compute_cost(self.weight, 1, 0, 0)
        self.assertEqual(total, 10.0)

    def test_05_value_cost(self):
        total = self.Carrier.compute_cost(self.value, 0, 0, 1000)
        self.assertEqual(total, 50.0)

    def test_06_cost_record_estimated(self):
        cost = self.Cost.create({
            'carrier_id': self.weight.id,
            'weight': 40.0,
        })
        self.assertEqual(cost.total_cost, 100.0)
        self.assertEqual(cost.state, 'estimated')

    def test_07_mark_actual(self):
        cost = self.Cost.create({'carrier_id': self.fixed.id})
        cost.action_mark_actual()
        self.assertEqual(cost.state, 'actual')

    def test_08_carrier_code_unique(self):
        with self.assertRaises(Exception):
            self.Carrier.create({
                'name': 'Dup', 'code': 'FIX', 'cost_method': 'fixed'})