# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSalesCommission(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env.ref('base.user_admin')
        cls.partner = cls.env['res.partner'].create({
            'name': 'Commission Customer',
            'user_id': cls.user.id,
        })
        cls.product = cls.env['product.product'].create({
            'name': 'Commission Product',
            'type': 'consu',
            'list_price': 100.0,
            'standard_price': 40.0,
        })

    def _new_plan(self, rate=5.0, calc='gross'):
        return self.env['sf.commission.plan'].create({
            'name': 'Standard Plan',
            'rate': rate,
            'calculation_type': calc,
        })

    def _new_line(self, plan, base=1000.0, rate=None, salesperson=None):
        return self.env['sf.commission.line'].create({
            'name': 'L-0001',
            'salesperson_id': salesperson.id if salesperson else self.user.id,
            'plan_id': plan.id,
            'base_amount': base,
            'rate': rate if rate is not None else plan.rate,
            'state': 'draft',
        })

    def test_01_plan_create(self):
        plan = self._new_plan(rate=7.5)
        self.assertEqual(plan.rate, 7.5)
        self.assertEqual(plan.calculation_type, 'gross')
        self.assertTrue(plan.active)

    def test_02_commission_compute(self):
        plan = self._new_plan(rate=5.0)
        line = self._new_line(plan, base=1000.0)
        self.assertEqual(line.commission, 50.0)
        self.assertEqual(line.final_commission, 50.0)

    def test_03_adjustment(self):
        plan = self._new_plan(rate=5.0)
        line = self._new_line(plan, base=1000.0)
        line.adjustment = 10.0
        self.assertEqual(line.final_commission, 60.0)
        line.adjustment = -15.0
        self.assertEqual(line.final_commission, 35.0)

    def test_04_negative_rate_rejected(self):
        with self.assertRaises(ValidationError):
            self.env['sf.commission.plan'].create({
                'name': 'Bad Plan',
                'rate': -1.0,
                'calculation_type': 'gross',
            })

    def test_05_workflow(self):
        plan = self._new_plan(rate=10.0)
        line = self._new_line(plan, base=500.0)
        self.assertEqual(line.state, 'draft')
        line.action_approve()
        self.assertEqual(line.state, 'approved')
        line.action_paid()
        self.assertEqual(line.state, 'paid')
        line.action_cancel()
        self.assertEqual(line.state, 'cancelled')
        line.action_draft()
        self.assertEqual(line.state, 'draft')

    def test_06_rule_target_required(self):
        plan = self._new_plan()
        with self.assertRaises(ValidationError):
            self.env['sf.commission.rule'].create({
                'plan_id': plan.id,
                'rate': 3.0,
            })

    def test_07_generate_from_sale_order(self):
        plan = self._new_plan(rate=5.0)
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'user_id': self.user.id,
            'order_line': [(0, 0, {
                'product_id': self.product.id,
                'product_uom_qty': 10,
                'price_unit': 100.0,
            })],
        })
        order.action_confirm()
        order.action_generate_commission()
        self.assertTrue(order.commission_line_ids)
        self.assertEqual(len(order.commission_line_ids), 1)
        line = order.commission_line_ids[0]
        self.assertEqual(line.salesperson_id.id, self.user.id)
        self.assertEqual(line.rate, 5.0)
        self.assertAlmostEqual(line.base_amount, order.amount_total, places=1)
        self.assertAlmostEqual(line.commission,
                               order.amount_total * 0.05, places=1)
        self.assertAlmostEqual(order.total_commission,
                               order.amount_total * 0.05, places=1)