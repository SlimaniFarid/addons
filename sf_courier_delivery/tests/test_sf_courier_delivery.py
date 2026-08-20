# -*- coding: utf-8 -*-
import uuid

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfCourierDelivery(TransactionCase):

    def setUp(self):
        super().setUp()
        self.todo_type = self.env.ref('mail.mail_activity_data_todo')
        self.courier = self.env['res.partner'].create({
            'name': 'Courier %s' % uuid.uuid4().hex[:6],
            'is_company': False,
        })
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def _create_order(self, state='confirmed'):
        return self.env['sf.courier.order'].create({
            'partner_id': self.customer.id,
            'type': 'pickup_delivery',
            'state': state,
        })

    def _create_route(self):
        return self.env['sf.courier.route'].create({
            'courier_id': self.courier.id,
        })

    def _create_delivery(self, order, state='draft'):
        vals = {
            'order_id': order.id,
            'courier_id': self.courier.id,
            'state': state,
        }
        if state == 'assigned':
            vals['route_id'] = self._create_route().id
        return self.env['sf.courier.delivery'].create(vals)

    def _pending_todos(self, record):
        return record.activity_ids.filtered(
            lambda a: a.activity_type_id == self.todo_type and not a.done
        )

    def test_sequences(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        self.assertTrue(order.name.startswith('CR-'))
        self.assertTrue(delivery.name.startswith('DLV-'))

    def test_order_workflow(self):
        order = self._create_order('draft')
        order.action_confirm()
        self.assertEqual(order.state, 'confirmed')
        order.action_done()
        self.assertEqual(order.state, 'done')

    def test_delivery_workflow(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        self.assertEqual(delivery.state, 'assigned')
        route = self._create_route()
        delivery.route_id = route.id
        delivery.action_start()
        self.assertEqual(delivery.state, 'in_transit')
        delivery.write({'proof_type': 'signature', 'proof_signature': b'x'})
        delivery.action_deliver()
        self.assertEqual(delivery.state, 'delivered')
        self.assertTrue(delivery.delivery_date)

    def test_delivery_requires_proof(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        route = self._create_route()
        delivery.route_id = route.id
        delivery.action_start()
        with self.assertRaises(UserError):
            delivery.action_deliver()

    def test_delivery_requires_route(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        with self.assertRaises(UserError):
            delivery.action_start()

    def test_failure_retry_and_return(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        route = self._create_route()
        delivery.route_id = route.id
        delivery.action_start()
        delivery.action_fail('absent')
        self.assertEqual(delivery.state, 'failed')
        delivery.action_retry()
        self.assertEqual(delivery.state, 'in_transit')
        delivery.action_fail('refused')
        with self.assertRaises(UserError):
            delivery.action_retry()
        delivery.action_return()
        self.assertEqual(delivery.state, 'returned')
        self.assertTrue(delivery.return_date)

    def test_delivered_immutable(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        route = self._create_route()
        delivery.route_id = route.id
        delivery.action_start()
        delivery.write({'proof_type': 'photo', 'proof_photo': b'x'})
        delivery.action_deliver()
        with self.assertRaises(UserError):
            delivery.write({'price': 99.0})

    def test_cancel_delivered_impossible(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        route = self._create_route()
        delivery.route_id = route.id
        delivery.action_start()
        delivery.write({'proof_type': 'signature', 'proof_signature': b'x'})
        delivery.action_deliver()
        with self.assertRaises(UserError):
            delivery.action_cancel()

    def test_route_close_requires_all_closed(self):
        order = self._create_order()
        route = self._create_route()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        delivery.route_id = route.id
        route.action_plan()
        route.action_start()
        with self.assertRaises(UserError):
            route.action_done()

    def test_route_workflow(self):
        order = self._create_order()
        route = self._create_route()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        delivery.route_id = route.id
        route.action_plan()
        self.assertEqual(route.state, 'planned')
        route.action_start()
        self.assertEqual(route.state, 'in_progress')
        self.assertEqual(delivery.state, 'in_transit')
        delivery.write({'proof_type': 'signature', 'proof_signature': b'x'})
        delivery.action_deliver()
        route.action_done()
        self.assertEqual(route.state, 'done')

    def test_cron_alerts_dedup(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        delivery.action_assign()
        order.scheduled_to = fields.Datetime.now()
        delivery.order_id.scheduled_to = fields.Datetime.now()
        order._cron_daily_alerts()
        order._cron_daily_alerts()
        self.assertEqual(len(self._pending_todos(delivery)), 1)

    def test_report_generation(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        records = {
            'action_report_delivery_ticket': delivery,
            'action_report_collection_note': order,
            'action_report_disputes_list': delivery,
            'action_report_activity': delivery,
        }
        for report, record in records.items():
            action = self.env.ref('sf_courier_delivery.%s' % report).report_action(record)
            self.assertTrue(action)

    def test_invoicing(self):
        order = self._create_order()
        delivery = self._create_delivery(order)
        delivery.price = 25.0
        delivery.action_assign()
        route = self._create_route()
        delivery.route_id = route.id
        delivery.action_start()
        delivery.write({'proof_type': 'signature', 'proof_signature': b'x'})
        delivery.action_deliver()
        order.action_invoice()
        self.assertTrue(order.invoice_id)
        self.assertEqual(order.invoice_id.amount_total, 25.0)
        with self.assertRaises(UserError):
            order.action_invoice()

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Second Co'})
        order1 = self._create_order()
        order2 = self.env['sf.courier.order'].with_company(company2).create({
            'partner_id': self.customer.id,
            'type': 'pickup_delivery',
            'company_id': company2.id,
        })
        user = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref('sf_courier_delivery.group_sf_courier_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
        })
        self.assertTrue(order1.with_user(user).exists())
        self.assertFalse(order2.with_user(user).exists())