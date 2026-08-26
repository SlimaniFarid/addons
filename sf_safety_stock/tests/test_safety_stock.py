# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestSafetyStock(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Rule = self.env['sf.safety.stock.rule']
        self.Demand = self.env['sf.safety.stock.demand']
        self.Product = self.env['product.product']
        self.Warehouse = self.env['stock.warehouse']
        self.product = self.Product.create({
            'name': 'Widget',
            'type': 'product',
        })
        self.warehouse = self.Warehouse.search([], limit=1)

    def test_01_rule_creation(self):
        rule = self.Rule.create({
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'service_level': '95',
            'demand_days': 30,
            'lead_time_days': 7,
        })
        self.assertEqual(rule.service_level, '95')
        self.assertEqual(rule.demand_days, 30)
        self.assertEqual(rule.lead_time_days, 7)

    def test_02_rule_required_warehouse(self):
        with self.assertRaises(Exception):
            self.Rule.create({'product_id': self.product.id})

    def test_03_demand_line(self):
        rule = self.Rule.create({
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
        })
        line = self.Demand.create({
            'rule_id': rule.id,
            'day': '2026-01-10',
            'quantity': 50.0,
        })
        self.assertEqual(line.quantity, 50.0)

    def test_04_demand_unique_per_day(self):
        rule = self.Rule.create({
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
        })
        self.Demand.create({
            'rule_id': rule.id, 'day': '2026-01-10', 'quantity': 10.0,
        })
        with self.assertRaises(Exception):
            self.Demand.create({
                'rule_id': rule.id, 'day': '2026-01-10', 'quantity': 20.0,
            })

    def test_05_safety_stock_zero_without_demand(self):
        rule = self.Rule.create({
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'demand_days': 30,
            'lead_time_days': 7,
            'service_level': '95',
        })
        self.assertEqual(rule.safety_stock, 0.0)
        self.assertEqual(rule.reorder_point, 0.0)

    def test_06_safety_stock_from_demand(self):
        rule = self.Rule.create({
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'demand_days': 10,
            'lead_time_days': 4,
            'service_level': '95',
        })
        for day in range(1, 11):
            self.Demand.create({
                'rule_id': rule.id,
                'day': '2026-02-%02d' % day,
                'quantity': 10.0,
            })
        # avg daily = 100/10 = 10, lead=4, z=1.65
        # safety = 10 * 1.65 * sqrt(4) = 33.0
        self.assertEqual(rule.safety_stock, 33.0)
        # reorder = 10*4 + 33 = 73.0
        self.assertEqual(rule.reorder_point, 73.0)

    def test_07_suggested_quantity(self):
        rule = self.Rule.create({
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'demand_days': 10,
            'lead_time_days': 4,
            'service_level': '90',
        })
        for day in range(1, 11):
            self.Demand.create({
                'rule_id': rule.id,
                'day': '2026-03-%02d' % day,
                'quantity': 10.0,
            })
        # z=1.28, safety = 10*1.28*2 = 25.6, reorder=40+25.6=65.6
        rule.current_stock = 40.0
        self.assertEqual(rule.suggested_qty, 25.6)

    def test_08_below_point_flag(self):
        rule = self.Rule.create({
            'product_id': self.product.id,
            'warehouse_id': self.warehouse.id,
            'demand_days': 10,
            'lead_time_days': 4,
            'service_level': '95',
        })
        for day in range(1, 11):
            self.Demand.create({
                'rule_id': rule.id,
                'day': '2026-04-%02d' % day,
                'quantity': 10.0,
            })
        # reorder point 73.0, current stock 0 -> below
        self.assertTrue(rule.below_point)
        rule.current_stock = 100.0
        self.assertFalse(rule.below_point)