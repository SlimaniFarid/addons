# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestHotelPms(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Room = self.env['sf.hotel.room']
        self.Reservation = self.env['sf.hotel.reservation']
        self.Extra = self.env['sf.hotel.extra']
        self.Housekeeping = self.env['sf.hotel.housekeeping']
        self.group_user = self.env.ref('sf_hotel_pms.group_sf_hotel_user')
        self.group_manager = self.env.ref(
            'sf_hotel_pms.group_sf_hotel_manager')
        self.user = self.env['res.users'].create({
            'name': 'Hotel Reception',
            'login': 'hotel_reception',
            'groups_id': [(4, self.group_user.id)],
        })
        self.manager = self.env['res.users'].create({
            'name': 'Hotel Manager',
            'login': 'hotel_manager',
            'groups_id': [(4, self.group_manager.id)],
        })

    def _create_room(self, **kwargs):
        values = {
            'number': 101,
            'room_type': 'double',
            'capacity': 2,
            'base_price': 100.0,
        }
        values.update(kwargs)
        return self.Room.create(values)

    def _create_reservation(self, **kwargs):
        values = {
            'guest_name': 'John Doe',
            'check_in': fields.Date.today(),
            'check_out': fields.Date.today() + timedelta(days=3),
        }
        values.update(kwargs)
        return self.Reservation.create(values)

    def test_create_models_with_sequences(self):
        room = self._create_room()
        self.assertTrue(room.name.startswith('ROM-'))
        reservation = self._create_reservation()
        self.assertTrue(reservation.name.startswith('RES-'))
        extra = self.Extra.create({
            'reservation_id': reservation.id,
            'description': 'Minibar',
            'amount': 15.0,
        })
        self.assertTrue(extra.name.startswith('EXT-'))
        housekeeping = self.Housekeeping.create({
            'room_id': room.id,
            'date': fields.Date.today(),
            'task_type': 'cleaning',
        })
        self.assertTrue(housekeeping.name.startswith('HSK-'))

    def test_nights_and_total_computation(self):
        room = self._create_room(base_price=100.0)
        reservation = self._create_reservation(
            room_ids=[(6, 0, [room.id])])
        self.assertEqual(reservation.nights, 3)
        self.assertEqual(reservation.total, 300.0)
        extra = self.Extra.create({
            'reservation_id': reservation.id,
            'description': 'Minibar',
            'amount': 20.0,
        })
        extra.with_user(self.manager).action_charge()
        self.assertEqual(extra.state, 'charged')
        self.assertEqual(reservation.total, 320.0)

    def test_anti_overbooking(self):
        room = self._create_room()
        first = self._create_reservation(
            room_ids=[(6, 0, [room.id])])
        first.action_reservation_confirm()
        self.assertEqual(first.status, 'confirmed')
        self.assertEqual(room.status, 'reserved')
        second = self._create_reservation(
            room_ids=[(6, 0, [room.id])])
        with self.assertRaises(UserError):
            second.action_reservation_confirm()

    def test_no_overbooking_on_non_overlapping_period(self):
        room = self._create_room()
        first = self._create_reservation(
            room_ids=[(6, 0, [room.id])])
        first.action_reservation_confirm()
        second = self._create_reservation(
            check_in=fields.Date.today() + timedelta(days=5),
            check_out=fields.Date.today() + timedelta(days=8),
            room_ids=[(6, 0, [room.id])])
        second.action_reservation_confirm()
        self.assertEqual(second.status, 'confirmed')

    def test_check_in_check_out_manager_only(self):
        room = self._create_room()
        reservation = self._create_reservation(
            room_ids=[(6, 0, [room.id])])
        reservation.action_reservation_confirm()
        with self.assertRaises(UserError):
            reservation.with_user(self.user).action_check_in()
        reservation.with_user(self.manager).action_check_in()
        self.assertEqual(reservation.status, 'checked_in')
        self.assertEqual(room.status, 'occupied')
        with self.assertRaises(UserError):
            reservation.with_user(self.user).action_check_out()
        reservation.with_user(self.manager).action_check_out()
        self.assertEqual(reservation.status, 'checked_out')
        self.assertEqual(room.status, 'available')

    def test_extra_charge_manager_only(self):
        reservation = self._create_reservation()
        extra = self.Extra.create({
            'reservation_id': reservation.id,
            'description': 'Room service',
            'amount': 25.0,
        })
        with self.assertRaises(UserError):
            extra.with_user(self.user).action_charge()
        extra.with_user(self.manager).action_charge()
        self.assertEqual(extra.state, 'charged')

    def test_housekeeping_done_manager_only(self):
        room = self._create_room()
        task = self.Housekeeping.create({
            'room_id': room.id,
            'date': fields.Date.today(),
            'task_type': 'cleaning',
        })
        task.action_plan()
        self.assertEqual(task.state, 'planned')
        with self.assertRaises(UserError):
            task.with_user(self.user).action_done()
        task.with_user(self.manager).action_done()
        self.assertEqual(task.state, 'done')

    def test_cron_departure_alert_dedup(self):
        room = self._create_room()
        reservation = self._create_reservation(
            check_in=fields.Date.today() - timedelta(days=2),
            check_out=fields.Date.today(),
            room_ids=[(6, 0, [room.id])])
        reservation.action_reservation_confirm()
        self.Reservation._check_departures_and_housekeeping()
        self.Reservation._check_departures_and_housekeeping()
        activities = reservation.activity_ids.filtered(
            lambda activity: activity.activity_type_id ==
            self.env.ref('mail.mail_activity_data_todo'))
        self.assertEqual(len(activities), 1)

    def test_cron_housekeeping_alert_dedup(self):
        room = self._create_room()
        reservation = self._create_reservation(
            room_ids=[(6, 0, [room.id])])
        reservation.action_reservation_confirm()
        reservation.with_user(self.manager).action_check_in()
        self.assertEqual(room.status, 'occupied')
        self.Reservation._check_departures_and_housekeeping()
        self.Reservation._check_departures_and_housekeeping()
        activities = room.activity_ids.filtered(
            lambda activity: activity.activity_type_id ==
            self.env.ref('mail.mail_activity_data_todo'))
        self.assertEqual(len(activities), 1)

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create(
            {'name': 'Hotel Company B'})
        room_b = self.Room.with_company(company_b).create({
            'number': 201,
            'room_type': 'double',
            'base_price': 90.0,
        })
        self.assertNotIn(room_b, self.Room.with_user(self.user).search(
            [('id', '=', room_b.id)]))
        self.assertIn(room_b, self.Room.with_user(self.manager).search(
            [('id', '=', room_b.id)]))

    def test_reports_render(self):
        room = self._create_room()
        reservation = self._create_reservation(
            room_ids=[(6, 0, [room.id])])
        reservation.action_reservation_confirm()
        res_report = self.env.ref(
            'sf_hotel_pms.report_reservation_confirmation')
        self.assertEqual(res_report.report_type, 'qweb-pdf')
        content, _ = res_report._render_qweb_pdf(reservation.id)
        self.assertTrue(content)
        room_report = self.env.ref(
            'sf_hotel_pms.report_occupation_housekeeping')
        self.assertEqual(room_report.report_type, 'qweb-pdf')
        content, _ = room_report._render_qweb_pdf(room.id)
        self.assertTrue(content)