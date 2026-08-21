# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfReworkManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.product = self.env['product.product'].create({
            'name': 'Product %s' % uuid.uuid4().hex[:6],
            'standard_price': 10.0,
        })
        self.manager_group = self.env.ref(
            'sf_rework_management.group_sf_rework_management_manager')
        self.user_group = self.env.ref(
            'sf_rework_management.group_sf_rework_management_user')
        self.manager = self.env['res.users'].create({
            'name': 'Rework Manager',
            'login': 'rework_mgr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.manager_group.id])],
        })
        self.user = self.env['res.users'].create({
            'name': 'Rework User',
            'login': 'rework_usr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.user_group.id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })

    def _create_order(self, **kw):
        vals = {
            'product_id': self.product.id,
            'qty': 10.0,
            'source': 'production',
            'reason': 'Assembly error',
            'hourly_rate': 20.0,
        }
        vals.update(kw)
        return self.env['sf.rework.order'].create(vals)

    def _add_operation(self, order, hours=2.0, hourly_rate=20.0):
        return self.env['sf.rework.operation'].create({
            'order_id': order.id,
            'name': 'Repair',
            'hours': hours,
            'hourly_rate': hourly_rate,
        })

    def _add_scrap(self, order, qty=2.0, unit_value=5.0):
        return self.env['sf.rework.scrap'].create({
            'order_id': order.id,
            'product_id': self.product.id,
            'qty': qty,
            'unit_value': unit_value,
            'scrap_reason': 'Damaged',
        })

    def test_sequence(self):
        order = self._create_order()
        self.assertTrue(order.name.startswith('RWO-'))

    def test_currency_id_defaults(self):
        order = self.env['sf.rework.order'].create({
            'product_id': self.product.id,
            'qty': 5.0,
            'hourly_rate': 15.5,
            'source': 'production',
            'reason': 'Test',
        })
        self.assertEqual(order.currency_id, self.env.company.currency_id)
        self.assertEqual(order.hourly_rate, 15.5)

        op = self._add_operation(order)
        self.assertEqual(op.currency_id, self.env.company.currency_id)

        sc = self._add_scrap(order)
        self.assertEqual(sc.currency_id, self.env.company.currency_id)

    def test_cost_computation(self):
        order = self._create_order()
        self._add_operation(order, 2.0, 20.0)
        self._add_operation(order, 1.5, 25.0)
        self._add_scrap(order, 2.0, 5.0)
        self._add_scrap(order, 1.0, 10.0)
        self.assertEqual(order.total_hours, 3.5)
        self.assertEqual(order.rework_cost, 2.0 * 20.0 + 1.5 * 25.0)
        self.assertEqual(order.scrap_value, 2.0 * 5.0 + 1.0 * 10.0)
        self.assertEqual(order.total_cost, order.rework_cost + order.scrap_value)

    def test_workflow(self):
        order = self._create_order()
        order.action_start()
        self.assertEqual(order.state, 'in_progress')
        self.assertTrue(order.actual_start_datetime)
        order.action_complete()
        self.assertEqual(order.state, 'completed')
        self.assertTrue(order.actual_end_datetime)
        order.with_user(self.manager).action_close()
        self.assertEqual(order.state, 'closed')

    def test_bad_transitions(self):
        order = self._create_order()
        with self.assertRaises(UserError):
            order.action_complete()
        order.action_start()
        with self.assertRaises(UserError):
            order.action_start()

    def test_user_cannot_cancel_or_close(self):
        order = self._create_order()
        with self.assertRaises(UserError):
            order.with_user(self.user).action_cancel()
        order.action_start()
        order.action_complete()
        with self.assertRaises(UserError):
            order.with_user(self.user).action_close()

    def test_manager_can_cancel(self):
        order = self._create_order()
        order.with_user(self.manager).action_cancel()
        self.assertEqual(order.state, 'cancelled')

    def test_quantity_constraint(self):
        with self.assertRaises(ValidationError):
            self._create_order(qty=0)

    def test_operation_hours_constraint(self):
        order = self._create_order()
        with self.assertRaises(ValidationError):
            self.env['sf.rework.operation'].create({
                'order_id': order.id,
                'name': 'Repair',
                'hours': -1,
                'hourly_rate': 10.0,
            })
        op = self.env['sf.rework.operation'].create({
            'order_id': order.id,
            'name': 'Inspection',
            'hours': 0,
            'hourly_rate': 10.0,
        })
        self.assertEqual(op.hours, 0)

    def test_scrap_qty_constraint(self):
        order = self._create_order()
        with self.assertRaises(ValidationError):
            self.env['sf.rework.scrap'].create({
                'order_id': order.id,
                'product_id': self.product.id,
                'qty': 0,
                'unit_value': 5.0,
                'scrap_reason': 'Test',
            })

    def test_cron_escalation(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'sf_rework_management.alert_days', '7')
        old = self._create_order()
        old.action_start()
        old.with_context(allow_write_on_locked=True).write(
            {'actual_start_datetime': fields.Datetime.now() - timedelta(days=10)})
        fresh = self._create_order()
        fresh.action_start()
        self.env['sf.rework.order']._cron_escalation()
        self.assertTrue(old.activity_ids)
        self.assertFalse(fresh.activity_ids)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Rework Co 2'})
        order2 = self.env['sf.rework.order'].with_company(company2).create({
            'product_id': self.product.id,
            'qty': 5.0,
            'hourly_rate': 20.0,
            'source': 'production',
            'reason': 'Test',
            'company_id': company2.id,
        })
        visible = self.env['sf.rework.order'].with_user(self.user).search(
            [('id', '=', order2.id)])
        self.assertFalse(visible)

    def test_write_guard_on_locked_states(self):
        order = self._create_order()
        order.action_start()
        order.action_complete()
        with self.assertRaises(UserError):
            order.write({'reason': 'Changed after completion'})
        with self.assertRaises(UserError):
            order.with_user(self.user).write({'reason': 'Changed by user'})
        order.with_user(self.manager).with_context(allow_write_on_locked=True).write(
            {'reason': 'Changed by manager with context'})
        self.assertEqual(order.reason, 'Changed by manager with context')

    def test_report_generation(self):
        order = self._create_order()
        self._add_operation(order, 1.0)
        action = self.env.ref(
            'sf_rework_management.action_report_rework_order').report_action(order)
        self.assertTrue(action)