# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfLaundry(TransactionCase):

    def setUp(self):
        super().setUp()
        self.today = fields.Date.today()
        self.todo_type = self.env.ref('mail.mail_activity_data_todo')

    def _create_order(self, customer=None, state='draft', expected=None):
        vals = {
            'customer_name': customer or 'Test Customer %s' % uuid.uuid4().hex[:6],
            'phone': '555-0100',
            'deposit_date': self.today,
            'state': state,
        }
        if expected:
            vals['expected_delivery_date'] = expected
        return self.env['sf.laundry.order'].create(vals)

    def _create_item(self, order, qty=1, price=5.0, item_type=None, service='wash', state='received'):
        vals = {
            'order_id': order.id,
            'service': service,
            'qty': qty,
            'price_unit': price,
            'state': state,
        }
        if item_type:
            vals['item_type'] = item_type.id if hasattr(item_type, 'id') else item_type
        return self.env['sf.laundry.item'].create(vals)

    def _create_item_type(self, name='Shirt', service='wash', price=4.5):
        return self.env['sf.laundry.item.type'].create({
            'name': name,
            'service': service,
            'price_unit': price,
        })

    def _pending_todos(self, record):
        return record.activity_ids.filtered(
            lambda a: a.activity_type_id == self.todo_type and not a.done
        )

    def test_sequences(self):
        order = self._create_order()
        item = self._create_item(order)
        self.assertTrue(order.name.startswith('LD-'))
        self.assertTrue(item.name.startswith('LI-'))

    def test_default_price_from_item_type(self):
        item_type = self._create_item_type('Dress', 'dry_clean', 12.0)
        order = self._create_order()
        item = self.env['sf.laundry.item'].create({
            'order_id': order.id,
            'item_type': item_type.id,
            'service': 'dry_clean',
            'qty': 2,
        })
        self.assertEqual(item.price_unit, 12.0)
        self.assertEqual(item.subtotal, 24.0)

    def test_default_expected_delivery_date(self):
        order = self._create_order()
        self.assertEqual(order.expected_delivery_date, self.today + timedelta(days=3))

    def test_order_workflow(self):
        order = self._create_order()
        self._create_item(order)
        order.action_receive()
        self.assertEqual(order.state, 'received')
        order.action_start()
        self.assertEqual(order.state, 'in_progress')
        order.action_ready()
        self.assertEqual(order.state, 'ready')
        order.action_deliver()
        self.assertEqual(order.state, 'delivered')
        self.assertTrue(order.delivery_date)

    def test_receive_requires_items(self):
        order = self._create_order()
        with self.assertRaises(UserError):
            order.action_receive()

    def test_lost_item_blocks_delivery(self):
        order = self._create_order()
        item = self._create_item(order)
        order.action_receive()
        order.action_start()
        item.action_mark_lost()
        order.action_ready()
        with self.assertRaises(UserError):
            order.action_deliver()

    def test_regularize_lost_item(self):
        order = self._create_order()
        item = self._create_item(order)
        order.action_receive()
        item.action_mark_lost()
        self.assertEqual(item.state, 'lost')
        item.action_regularize()
        self.assertEqual(item.state, 'in_progress')

    def test_cancel_received_requires_manager(self):
        order = self._create_order()
        self._create_item(order)
        order.action_receive()
        company = self.env.company
        user = self.env['res.users'].create({
            'name': 'Laundry User %s' % uuid.uuid4().hex[:6],
            'login': 'laundry_user_%s' % uuid.uuid4().hex[:8],
            'company_id': company.id,
            'company_ids': [(6, 0, [company.id])],
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.env.ref('sf_laundry.group_sf_laundry_user').id),
            ],
        })
        with self.assertRaises(UserError):
            order.with_user(user).action_cancel()

    def test_cancel_delivered_impossible(self):
        order = self._create_order()
        self._create_item(order)
        order.action_receive()
        order.action_start()
        order.action_ready()
        order.action_deliver()
        with self.assertRaises(UserError):
            order.action_cancel()

    def test_delivered_items_immutable(self):
        order = self._create_order()
        item = self._create_item(order)
        order.action_receive()
        order.action_start()
        order.action_ready()
        order.action_deliver()
        with self.assertRaises(UserError):
            order.write({'item_ids': [(1, item.id, {'qty': 5})]})

    def test_negative_quantity_blocked(self):
        order = self._create_order()
        with self.assertRaises(UserError):
            self._create_item(order, qty=0)

    def test_cron_alerts_dedup(self):
        order = self._create_order(expected=self.today - timedelta(days=1))
        self._create_item(order)
        order.action_receive()
        order._cron_daily_alerts()
        order._cron_daily_alerts()
        self.assertEqual(len(self._pending_todos(order)), 1)

    def test_item_type_price_change_manager_only(self):
        item_type = self._create_item_type()
        company = self.env.company
        user = self.env['res.users'].create({
            'name': 'Laundry User2 %s' % uuid.uuid4().hex[:6],
            'login': 'laundry_user2_%s' % uuid.uuid4().hex[:8],
            'company_id': company.id,
            'company_ids': [(6, 0, [company.id])],
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.env.ref('sf_laundry.group_sf_laundry_user').id),
            ],
        })
        with self.assertRaises(UserError):
            item_type.with_user(user).write({'price_unit': 9.0})

    def test_report_generation(self):
        order = self._create_order()
        self._create_item(order)
        order.action_receive()
        for report in ['report_deposit_receipt', 'report_delivery_ticket']:
            action = self.env.ref('sf_laundry.%s' % report).report_action(order)
            self.assertTrue(action)