# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestVehicleWorkshop(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Vehicle = self.env['sf.workshop.vehicle']
        self.Request = self.env['sf.workshop.request']
        self.Order = self.env['sf.workshop.order']
        self.Operation = self.env['sf.workshop.operation']
        self.Part = self.env['sf.workshop.part']
        self.group_user = self.env.ref(
            'sf_vehicle_workshop.group_sf_workshop_user')
        self.group_manager = self.env.ref(
            'sf_vehicle_workshop.group_sf_workshop_manager')
        self.user = self.env['res.users'].create({
            'name': 'Workshop User',
            'login': 'workshop_user_test',
            'groups_id': [(4, self.group_user.id)],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Workshop Manager',
            'login': 'workshop_manager_test',
            'groups_id': [(4, self.group_manager.id)],
        })
        self.vehicle = self.Vehicle.create({
            'license_plate': 'AB-123-CD',
            'brand': 'Volkswagen',
            'model': 'Golf',
        })

    def _create_request(self, priority='normal', state='draft'):
        return self.Request.create({
            'vehicle_id': self.vehicle.id,
            'requester': 'John Doe',
            'priority': priority,
            'state': state,
        })

    def _create_order(self, state='draft'):
        return self.Order.create({
            'vehicle_id': self.vehicle.id,
            'request_id': self._create_request().id,
            'state': state,
        })

    def test_create_models_with_sequences(self):
        request = self._create_request()
        order = self._create_order()
        operation = self.Operation.create({
            'order_id': order.id,
            'operation_type': 'mechanical',
            'hours': 2.0,
        })
        part = self.Part.create({
            'order_id': order.id,
            'part_name': 'Brake pads',
            'quantity': 1.0,
            'unit_price': 25.0,
        })
        self.assertTrue(self.vehicle.name.startswith('VEH-'))
        self.assertTrue(request.name.startswith('REQ-'))
        self.assertTrue(order.name.startswith('ORD-'))
        self.assertTrue(operation.name.startswith('OPR-'))
        self.assertTrue(part.name.startswith('PRT-'))

    def test_part_total_and_order_cost(self):
        order = self._create_order()
        part = self.Part.create({
            'order_id': order.id,
            'part_name': 'Brake pads',
            'quantity': 2.0,
            'unit_price': 10.0,
        })
        operation = self.Operation.create({
            'order_id': order.id,
            'operation_type': 'mechanical',
            'hours': 3.0,
        })
        self.env.company.sf_workshop_hourly_rate = 50.0
        self.assertEqual(part.total, 20.0)
        self.assertEqual(order.total_cost, 20.0 + 3.0 * 50.0)

    def test_assign_request_by_non_manager(self):
        request = self._create_request()
        with self.assertRaises(UserError):
            request.with_user(self.user).action_assign()

    def test_assign_request_by_manager(self):
        request = self._create_request()
        request.with_user(self.manager).action_assign()
        self.assertEqual(request.state, 'assigned')

    def test_order_done_by_non_manager(self):
        order = self._create_order(state='in_progress')
        with self.assertRaises(UserError):
            order.with_user(self.user).action_done()

    def test_order_close_by_non_manager(self):
        order = self._create_order(state='done')
        with self.assertRaises(UserError):
            order.with_user(self.user).action_close()

    def test_order_done_by_manager(self):
        order = self._create_order(state='in_progress')
        order.with_user(self.manager).action_done()
        self.assertEqual(order.state, 'done')

    def test_cron_alert_dedup(self):
        request = self._create_request(priority='urgent')
        self.env.cr.execute(
            'UPDATE sf_workshop_request SET create_date = %s WHERE id = %s',
            (fields.Datetime.now() - timedelta(days=30), request.id))
        order = self._create_order()
        order.write({
            'planned_end': fields.Date.context_today(order)
            - timedelta(days=5),
        })
        self.env.company.sf_workshop_alert_days = 7
        self.Request._check_workshop_alerts()
        self.Request._check_workshop_alerts()
        self.assertEqual(len(request.activity_ids), 1)
        self.assertEqual(len(order.activity_ids), 1)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create(
            {'name': 'Workshop Company B'})
        other = self.Request.with_company(company_b).create({
            'vehicle_id': self.vehicle.id,
            'requester': 'Jane Doe',
            'priority': 'normal',
        })
        self.assertNotIn(other, self.Request.with_user(self.user).search(
            [('id', '=', other.id)]))

    def test_reports_render(self):
        order = self._create_order()
        self.Part.create({
            'order_id': order.id,
            'part_name': 'Oil filter',
            'quantity': 1.0,
            'unit_price': 15.0,
        })
        self.Operation.create({
            'order_id': order.id,
            'operation_type': 'diagnostic',
            'hours': 1.0,
        })
        order_report = self.env['ir.actions.report']._get_report_from_name(
            'sf_vehicle_workshop.repair_order_template')
        pdf, _format = order_report._render_qweb_pdf([order.id])
        self.assertTrue(pdf)
        vehicle_report = self.env['ir.actions.report']._get_report_from_name(
            'sf_vehicle_workshop.vehicle_cost_template')
        pdf2, _format2 = vehicle_report._render_qweb_pdf([self.vehicle.id])
        self.assertTrue(pdf2)