# -*- coding: utf-8 -*-
import uuid
from datetime import datetime, timedelta

from odoo import fields as odoo_fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfParkingManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })
        self.site = self.env['sf.parking.site'].create({
            'name': 'Downtown',
            'capacity': 10,
            'hourly_rate': 2.0,
            'daily_rate': 12.0,
        })
        self.zone = self.env['sf.parking.zone'].create({
            'name': 'A',
            'site_id': self.site.id,
            'capacity': 5,
        })
        self.place = self.env['sf.parking.place'].create({
            'name': 'A-01',
            'zone_id': self.zone.id,
            'number': '1',
        })
        self.sale_journal = self.env['account.journal'].create({
            'name': 'Parking Test Sales',
            'type': 'sale',
            'code': 'PSJ',
        })
        self.income_account = self.env['account.account'].create({
            'name': 'Parking Revenue',
            'code': '400000',
            'account_type': 'income',
        })

    def _create_ticket(self, state='draft', hours=3):
        now = datetime.now().replace(second=0, microsecond=0)
        vals = {
            'site_id': self.site.id,
            'vehicle_plate': 'AB-123-CD',
            'state': state,
        }
        if state in ('open', 'closed', 'paid'):
            vals['entry_datetime'] = now
            if state in ('closed', 'paid'):
                vals['exit_datetime'] = now + timedelta(hours=hours)
        return self.env['sf.parking.ticket'].create(vals)

    def _create_subscription(self, **kw):
        vals = {
            'partner_id': self.customer.id,
            'site_id': self.site.id,
            'billing_period': 'monthly',
            'amount': 40.0,
            'start_date': odoo_fields.Date.today(),
        }
        vals.update(kw)
        return self.env['sf.parking.subscription'].create(vals)

    def test_sequences(self):
        site = self.env['sf.parking.site'].create({'capacity': 5})
        self.assertTrue(site.name.startswith('SIT-'))
        zone = self.env['sf.parking.zone'].create({'site_id': self.site.id, 'capacity': 2})
        self.assertTrue(zone.name.startswith('ZON-'))
        place = self.env['sf.parking.place'].create({'zone_id': zone.id})
        self.assertTrue(place.name.startswith('PLC-'))
        ticket = self._create_ticket()
        self.assertTrue(ticket.name.startswith('TKT-'))

    def test_site_default_rates(self):
        site = self.env['sf.parking.site'].create({'capacity': 5})
        self.assertEqual(site.hourly_rate, 2.0)
        self.assertEqual(site.daily_rate, 12.0)

    def test_ticket_amount_calculation(self):
        ticket = self._create_ticket('closed', hours=3)
        self.assertEqual(ticket.amount, 6.0)

    def test_ticket_daily_cap(self):
        ticket = self._create_ticket('closed', hours=20)
        self.assertEqual(ticket.amount, 12.0)

    def test_ticket_multi_day_cap(self):
        ticket = self._create_ticket('closed', hours=50)
        self.assertEqual(ticket.amount, 28.0)

    def test_ticket_workflow(self):
        ticket = self._create_ticket()
        ticket.action_open()
        self.assertEqual(ticket.state, 'open')
        ticket.action_close()
        self.assertEqual(ticket.state, 'closed')
        ticket.action_paid()
        self.assertEqual(ticket.state, 'paid')

    def test_exit_before_entry_blocked(self):
        ticket = self._create_ticket()
        ticket.action_open()
        now = datetime.now()
        with self.assertRaises(ValidationError):
            ticket.write({
                'entry_datetime': now,
                'exit_datetime': now - timedelta(hours=1),
            })

    def test_paid_ticket_immutable(self):
        ticket = self._create_ticket('paid', hours=1)
        with self.assertRaises(UserError):
            ticket.action_cancel()

    def test_ticket_place_workflow(self):
        ticket = self._create_ticket()
        ticket.place_id = self.place.id
        ticket.action_open()
        self.assertEqual(self.place.state, 'occupied')
        ticket.action_close()
        self.assertEqual(self.place.state, 'free')

    def test_ticket_place_occupied_blocked(self):
        ticket1 = self._create_ticket()
        ticket1.place_id = self.place.id
        ticket1.action_open()
        ticket2 = self._create_ticket()
        ticket2.place_id = self.place.id
        with self.assertRaises(UserError):
            ticket2.action_open()

    def test_ticket_place_out_of_service_blocked(self):
        self.place.state = 'out_of_service'
        with self.assertRaises(UserError):
            self.env['sf.parking.ticket'].create({
                'site_id': self.site.id,
                'place_id': self.place.id,
            })

    def test_subscription_workflow(self):
        subscription = self._create_subscription(place_id=self.place.id)
        self.assertTrue(subscription.name.startswith('SUB-'))
        subscription.action_activate()
        self.assertEqual(subscription.state, 'active')
        self.assertEqual(self.place.state, 'reserved')
        self.assertTrue(subscription.invoice_ids)

    def test_subscription_covers_ticket(self):
        subscription = self._create_subscription()
        subscription.action_activate()
        now = datetime.now().replace(second=0, microsecond=0)
        ticket = self.env['sf.parking.ticket'].create({
            'site_id': self.site.id,
            'vehicle_plate': 'AB-123-CD',
            'entry_datetime': now,
            'exit_datetime': now + timedelta(hours=3),
            'subscription_id': subscription.id,
            'state': 'closed',
        })
        self.assertEqual(ticket.amount, 0.0)

    def test_occupied_place_blocked(self):
        self.place.state = 'occupied'
        subscription = self._create_subscription(place_id=self.place.id)
        with self.assertRaises(UserError):
            subscription.action_activate()

    def test_renewal_workflow(self):
        today = odoo_fields.Date.today()
        start = today - timedelta(days=40)
        subscription = self._create_subscription(place_id=self.place.id, start_date=start)
        subscription.action_activate()
        self.assertEqual(self.place.state, 'reserved')
        subscription._cron_daily_checks()
        self.assertEqual(subscription.state, 'renewed')
        self.assertTrue(subscription.invoice_ids)
        self.assertGreater(subscription.end_date, today)
        self.assertEqual(self.place.state, 'reserved')

    def test_expired_subscription(self):
        subscription = self._create_subscription(place_id=self.place.id)
        subscription.action_activate()
        subscription._expire(self.env.ref('mail.mail_activity_data_todo'))
        self.assertEqual(subscription.state, 'expired')
        self.assertEqual(self.place.state, 'free')

    def test_occupancy_stats(self):
        self._create_ticket('open')
        self._create_ticket('open')
        self.assertEqual(self.site.open_tickets, 2)
        self.assertEqual(self.site.occupancy_rate, 20.0)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Parking Co 2'})
        site2 = self.env['sf.parking.site'].with_company(company2).create({
            'name': 'Site 2',
            'capacity': 5,
            'company_id': company2.id,
        })
        user = self.env['res.users'].create({
            'name': 'Parking User',
            'login': 'parking_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_parking_management.group_sf_parking_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.parking.site'].with_user(user).search([('id', '=', site2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        ticket = self._create_ticket('closed', hours=2)
        subscription = self._create_subscription()
        for report in ['action_report_ticket', 'action_report_revenue']:
            action = self.env.ref('sf_parking_management.%s' % report).report_action(ticket)
            self.assertTrue(action)
        action = self.env.ref('sf_parking_management.action_report_subscription').report_action(subscription)
        self.assertTrue(action)
        action = self.env.ref('sf_parking_management.action_report_occupancy').report_action(self.site)
        self.assertTrue(action)