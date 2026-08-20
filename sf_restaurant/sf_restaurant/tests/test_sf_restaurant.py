# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfRestaurant(TransactionCase):

    def setUp(self):
        super().setUp()
        self.today = fields.Date.today()
        self.todo_type = self.env.ref('mail.mail_activity_data_todo')

    def _create_zone(self, company=None):
        return self.env['sf.restaurant.zone'].create({
            'name': 'Test Zone %s' % uuid.uuid4().hex[:6],
            'company_id': (company or self.env.company).id,
        })

    def _create_table(self, zone, seats=4, company=None):
        return self.env['sf.restaurant.table'].create({
            'zone_id': zone.id,
            'seats': seats,
            'company_id': (company or self.env.company).id,
        })

    def _create_category(self, company=None):
        return self.env['sf.restaurant.menu.category'].create({
            'name': 'Test Category %s' % uuid.uuid4().hex[:6],
            'company_id': (company or self.env.company).id,
        })

    def _create_item(self, category, price=8.0, company=None, **kwargs):
        vals = {
            'name': 'Test Item %s' % uuid.uuid4().hex[:6],
            'category_id': category.id,
            'price_unit': price,
            'company_id': (company or self.env.company).id,
        }
        vals.update(kwargs)
        return self.env['sf.restaurant.menu.item'].create(vals)

    def _create_reservation(self, table, guests=2, company=None, date=None, start=12.0, state='draft'):
        return self.env['sf.restaurant.reservation'].create({
            'contact_name': 'Test Customer %s' % uuid.uuid4().hex[:6],
            'reservation_date': date or self.today,
            'start_time': start,
            'guests': guests,
            'table_ids': [(6, 0, [table.id])],
            'state': state,
            'company_id': (company or self.env.company).id,
        })

    def _create_order(self, table, service='lunch', company=None):
        return self.env['sf.restaurant.order'].create({
            'table_id': table.id,
            'service': service,
            'company_id': (company or self.env.company).id,
        })

    def _add_line(self, order, item, qty=1, price=None):
        vals = {
            'item_id': item.id,
            'qty': qty,
        }
        if price is not None:
            vals['price_unit'] = price
        return self.env['sf.restaurant.order.line'].create(dict(vals, order_id=order.id))

    def _create_user(self, company, manager=False):
        group_xmlid = 'sf_restaurant.group_sf_restaurant_manager' if manager else 'sf_restaurant.group_sf_restaurant_user'
        return self.env['res.users'].create({
            'name': 'Test Manager' if manager else 'Test User',
            'login': 'test_%s_%s' % ('manager' if manager else 'user', uuid.uuid4().hex[:8]),
            'company_id': company.id,
            'company_ids': [(6, 0, [company.id])],
            'groups_id': [
                (4, self.env.ref('base.group_user').id),
                (4, self.env.ref(group_xmlid).id),
            ],
        })

    def _pending_todos(self, record):
        return record.activity_ids.filtered(
            lambda a: a.activity_type_id == self.todo_type and not a.done
        )

    def test_create_sequences(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        category = self._create_category()
        item = self._create_item(category)
        reservation = self._create_reservation(table)
        order = self._create_order(table)
        self.assertTrue(zone.name.startswith('ZON-'))
        self.assertTrue(table.name.startswith('TAB-'))
        self.assertTrue(category.name.startswith('CAT-'))
        self.assertTrue(item.name.startswith('ITE-'))
        self.assertTrue(reservation.name.startswith('RES-'))
        self.assertTrue(order.name.startswith('CMD-'))

    def test_computed_totals(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        category = self._create_category()
        item = self._create_item(category, price=5.0)
        order = self._create_order(table)
        self._add_line(order, item, qty=2)
        self.assertEqual(order.total, 10.0)
        self.assertEqual(order.line_ids.subtotal, 10.0)

    def test_active_order_restriction(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        order = self._create_order(table)
        self.assertEqual(table.state, 'occupied')
        with self.assertRaises(UserError):
            self._create_order(table)

    def test_close_with_active_order(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        order = self._create_order(table)
        with self.assertRaises(UserError):
            order.action_close()

    def test_order_workflow(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        category = self._create_category()
        item = self._create_item(category, price=6.0)
        order = self._create_order(table)
        self._add_line(order, item, qty=1)
        order.action_transmit()
        self.assertEqual(order.state, 'transmitted')
        order.action_prepare()
        self.assertEqual(order.state, 'prepared')
        order.action_serve()
        self.assertEqual(order.state, 'served')
        order.action_close()
        self.assertEqual(order.state, 'closed')
        self.assertEqual(table.state, 'cleaning')

    def test_reservation_capacity_blocked(self):
        zone = self._create_zone()
        table = self._create_table(zone, seats=4)
        reservation = self._create_reservation(table, guests=4, state='confirmed')
        with self.assertRaises(UserError):
            self._create_reservation(table, guests=1, state='confirmed')

    def test_reservation_workflow(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        reservation = self._create_reservation(table, guests=2)
        reservation.action_confirm()
        self.assertEqual(reservation.state, 'confirmed')
        self.assertEqual(table.state, 'reserved')
        reservation.action_seat()
        self.assertEqual(reservation.state, 'seated')
        self.assertEqual(table.state, 'occupied')
        reservation.action_done()
        self.assertEqual(reservation.state, 'done')
        self.assertEqual(table.state, 'free')

    def test_item_unavailable_for_service(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        category = self._create_category()
        item = self._create_item(category, available_lunch=False)
        order = self._create_order(table, service='lunch')
        with self.assertRaises(UserError):
            self._add_line(order, item, qty=1)

    def test_cron_dedup(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        reservation = self._create_reservation(table, guests=2, state='confirmed')
        model = self.env['sf.restaurant.reservation']
        model._cron_daily_alerts()
        model._cron_daily_alerts()
        self.assertEqual(len(self._pending_todos(reservation)), 1)

    def test_multi_company_isolation(self):
        company_a = self.env['res.company'].create({'name': 'Company A %s' % uuid.uuid4().hex[:4]})
        company_b = self.env['res.company'].create({'name': 'Company B %s' % uuid.uuid4().hex[:4]})
        zone_a = self._create_zone(company=company_a)
        zone_b = self._create_zone(company=company_b)
        table_a = self._create_table(zone_a, company=company_a)
        table_b = self._create_table(zone_b, company=company_b)
        user = self._create_user(company_a)
        tables = self.env['sf.restaurant.table'].with_user(user.id).with_context(
            allowed_company_ids=[company_a.id]).search([('state', '=', 'free')])
        self.assertIn(table_a, tables)
        self.assertNotIn(table_b, tables)

    def test_multi_company_cron(self):
        company_a = self.env['res.company'].create({'name': 'Company A %s' % uuid.uuid4().hex[:4]})
        company_b = self.env['res.company'].create({'name': 'Company B %s' % uuid.uuid4().hex[:4]})
        zone_a = self._create_zone(company=company_a)
        zone_b = self._create_zone(company=company_b)
        table_a = self._create_table(zone_a, company=company_a)
        table_b = self._create_table(zone_b, company=company_b)
        reservation_a = self._create_reservation(table_a, guests=2, company=company_a, state='confirmed')
        reservation_b = self._create_reservation(table_b, guests=2, company=company_b, state='confirmed')
        self.env['sf.restaurant.reservation']._cron_daily_alerts()
        self.assertEqual(len(self._pending_todos(reservation_a)), 1)
        self.assertEqual(len(self._pending_todos(reservation_b)), 1)

    def test_manager_only_force_close(self):
        company = self.env['res.company'].create({'name': 'Company M %s' % uuid.uuid4().hex[:4]})
        zone = self._create_zone(company=company)
        table = self._create_table(zone, company=company)
        category = self._create_category(company=company)
        item = self._create_item(category, price=5.0, company=company)
        order = self._create_order(table, company=company)
        self._add_line(order, item, qty=1)
        order.action_transmit()
        user = self._create_user(company, manager=False)
        with self.assertRaises(UserError):
            order.with_user(user.id).with_context(allowed_company_ids=[company.id]).action_force_close()

    def test_report_generation(self):
        zone = self._create_zone()
        table = self._create_table(zone)
        category = self._create_category()
        item = self._create_item(category, price=7.0)
        order = self._create_order(table)
        self._add_line(order, item, qty=1)
        report = self.env.ref('sf_restaurant.report_kitchen_ticket')
        result = report._render_qweb_pdf(order.ids)
        self.assertTrue(result)
        self.assertNotEqual(result[1], 'html')