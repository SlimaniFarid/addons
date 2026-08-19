# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestProcessRouting(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Routing = self.env['sf.process.routing']
        self.Version = self.env['sf.process.routing.version']
        self.Route = self.env['sf.process.route']
        self.Condition = self.env['sf.process.routing.condition']
        self.Log = self.env['sf.process.routing.selection.log']
        self.product = self.env['product.product'].create({'name': 'Widget Pro'})
        self.wc1 = self.env['mrp.workcenter'].create({'name': 'CNC Mill', 'capacity': 100})
        self.wc2 = self.env['mrp.workcenter'].create({'name': 'Lathe', 'capacity': 80})
        self.bom = self.env['mrp.bom'].create({
            'product_tmpl_id': self.product.product_tmpl_id.id,
            'product_id': self.product.id,
            'product_qty': 1.0,
        })

    def test_01_routing_creation(self):
        routing = self.Routing.create({
            'product_id': self.product.id,
            'code': 'RT-001',
        })
        self.assertEqual(routing.code, 'RT-001')
        self.assertTrue(routing.active)

    def test_02_single_default_per_product(self):
        self.Routing.create({'product_id': self.product.id, 'code': 'RT-001', 'is_default': True})
        with self.assertRaises(Exception):
            self.Routing.create({'product_id': self.product.id, 'code': 'RT-002', 'is_default': True})

    def test_03_version_activation(self):
        routing = self.Routing.create({'product_id': self.product.id, 'code': 'RT-001'})
        v1 = self.Version.create({'routing_id': routing.id, 'version': '1.0'})
        v2 = self.Version.create({'routing_id': routing.id, 'version': '2.0'})
        v1.action_activate()
        self.assertEqual(v1.state, 'active')
        self.assertEqual(v2.state, 'draft')
        v2.action_activate()
        self.assertEqual(v2.state, 'active')
        self.assertEqual(v1.state, 'obsolete')

    def test_04_route_creation(self):
        routing = self.Routing.create({'product_id': self.product.id, 'code': 'RT-001'})
        version = self.Version.create({'routing_id': routing.id, 'version': '1.0'})
        route = self.Route.create({
            'version_id': version.id,
            'name': 'Standard Route',
            'bom_id': self.bom.id,
            'estimated_time': 5.0,
            'estimated_cost': 100.0,
        })
        self.assertEqual(route.estimated_time, 5.0)
        self.assertTrue(route.active)

    def test_05_condition_evaluation(self):
        routing = self.Routing.create({'product_id': self.product.id, 'code': 'RT-001'})
        version = self.Version.create({'routing_id': routing.id, 'version': '1.0'})
        route = self.Route.create({
            'version_id': version.id,
            'name': 'Test Route',
            'bom_id': self.bom.id,
            'estimated_time': 3.0,
            'estimated_cost': 50.0,
        })
        cond = self.Condition.create({
            'route_id': route.id,
            'condition_type': 'lead_time',
            'operator': '<=',
            'threshold': 4.0,
            'weight': 1.0,
        })
        context = {'quantity': 10}
        # lead_time = 3.0 <= 4.0 -> True
        self.assertTrue(cond.evaluate(context))

    def test_06_route_scoring(self):
        routing = self.Routing.create({'product_id': self.product.id, 'code': 'RT-001'})
        version = self.Version.create({'routing_id': routing.id, 'version': '1.0'})
        
        route1 = self.Route.create({
            'version_id': version.id, 'name': 'Fast Route', 'bom_id': self.bom.id,
            'estimated_time': 2.0, 'estimated_cost': 80.0,
        })
        route2 = self.Route.create({
            'version_id': version.id, 'name': 'Cheap Route', 'bom_id': self.bom.id,
            'estimated_time': 5.0, 'estimated_cost': 40.0,
        })
        
        cond1 = self.Condition.create({'route_id': route1.id, 'condition_type': 'lead_time', 'operator': '<=', 'threshold': 3.0, 'weight': 2.0})
        cond2 = self.Condition.create({'route_id': route2.id, 'condition_type': 'cost', 'operator': '<=', 'threshold': 50.0, 'weight': 2.0})
        
        # route1: lead_time=2.0 <= 3.0 -> True (weight 2)
        # route2: cost=40.0 <= 50.0 -> True (weight 2)
        # Both score 100%
        context = {'quantity': 10}
        self.assertEqual(route1.evaluate_conditions(context), 100.0)
        self.assertEqual(route2.evaluate_conditions(context), 100.0)

    def test_07_best_route_selection(self):
        routing = self.Routing.create({'product_id': self.product.id, 'code': 'RT-001'})
        version = self.Version.create({'routing_id': routing.id, 'version': '1.0'})
        version.action_activate()
        
        route1 = self.Route.create({
            'version_id': version.id, 'name': 'Fast Route', 'bom_id': self.bom.id,
            'estimated_time': 2.0, 'estimated_cost': 80.0, 'priority': 10,
        })
        route2 = self.Route.create({
            'version_id': version.id, 'name': 'Slow Route', 'bom_id': self.bom.id,
            'estimated_time': 10.0, 'estimated_cost': 50.0, 'priority': 5,
        })
        
        self.Condition.create({'route_id': route1.id, 'condition_type': 'lead_time', 'operator': '<=', 'threshold': 5.0, 'weight': 1.0})
        self.Condition.create({'route_id': route2.id, 'condition_type': 'lead_time', 'operator': '<=', 'threshold': 5.0, 'weight': 1.0})
        
        best = version.select_best_route(quantity=10)
        # Both pass condition, route1 has higher priority
        self.assertEqual(best, route1)

    def test_08_selection_log(self):
        routing = self.Routing.create({'product_id': self.product.id, 'code': 'RT-001'})
        version = self.Version.create({'routing_id': routing.id, 'version': '1.0'})
        route = self.Route.create({'version_id': version.id, 'name': 'Route', 'bom_id': self.bom.id})
        mo = self.env['mrp.production'].create({
            'product_id': self.product.id,
            'product_qty': 10,
            'bom_id': self.bom.id,
        })
        log = self.Log.create({
            'mo_id': mo.id,
            'routing_id': routing.id,
            'version_id': version.id,
            'route_id': route.id,
            'selection_method': 'auto',
            'score': 95.0,
        })
        self.assertEqual(log.mo_id, mo)
        self.assertEqual(log.score, 95.0)