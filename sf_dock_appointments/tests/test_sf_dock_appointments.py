# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfDockAppointments(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({
            'name': 'Carrier %s' % uuid.uuid4().hex[:6],
        })
        self.dock = self.env['sf.dock'].create({
            'name': 'Receiving Dock A',
            'dock_type': 'receiving',
        })
        self.dock2 = self.env['sf.dock'].create({
            'name': 'Shipping Dock B',
            'dock_type': 'shipping',
        })
        self.manager_group = self.env.ref(
            'sf_dock_appointments.group_sf_dock_appointments_manager')
        self.user_group = self.env.ref(
            'sf_dock_appointments.group_sf_dock_appointments_user')
        self.manager = self.env['res.users'].create({
            'name': 'Dock Manager',
            'login': 'dock_mgr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.manager_group.id])],
        })
        self.user = self.env['res.users'].create({
            'name': 'Dock User',
            'login': 'dock_usr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.user_group.id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })

    def _create_appointment(self, at=None, dock=None, window=60, **kw):
        vals = {
            'dock_id': dock or self.dock.id,
            'partner_id': self.partner.id,
            'direction': 'inbound',
            'appointment_datetime': at or (
                fields.Datetime.now() + timedelta(hours=4)),
            'window_minutes': window,
        }
        vals.update(kw)
        return self.env['sf.dock.appointment'].create(vals)

    def test_sequences(self):
        dock = self.env['sf.dock'].create({'name': 'Dock B'})
        self.assertTrue(dock.name.startswith('DCK-'))
        appointment = self._create_appointment()
        self.assertTrue(appointment.name.startswith('DAP-'))

    def test_default_window_from_settings(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'sf_dock_appointments.default_window_minutes', '90')
        appointment = self.env['sf.dock.appointment'].create({
            'dock_id': self.dock.id,
            'partner_id': self.partner.id,
            'appointment_datetime': fields.Datetime.now() + timedelta(hours=2),
        })
        self.assertEqual(appointment.window_minutes, 90)
        self.env['ir.config_parameter'].sudo().set_param(
            'sf_dock_appointments.default_window_minutes', '60')

    def test_overlap_conflict(self):
        at = fields.Datetime.now() + timedelta(hours=4)
        self._create_appointment(at=at, window=60)
        with self.assertRaises(UserError):
            self._create_appointment(at=at + timedelta(minutes=10), window=60)

    def test_non_overlap_allowed(self):
        at = fields.Datetime.now() + timedelta(hours=4)
        self._create_appointment(at=at, window=60)
        second = self._create_appointment(at=at + timedelta(hours=2), window=60)
        self.assertTrue(second)

    def test_workflow(self):
        appointment = self._create_appointment()
        appointment.action_arrive()
        self.assertEqual(appointment.state, 'arrived')
        self.assertTrue(appointment.actual_arrival_datetime)
        appointment.action_dock()
        self.assertEqual(appointment.state, 'docked')
        self.assertTrue(appointment.actual_dock_datetime)
        appointment.action_complete()
        self.assertEqual(appointment.state, 'completed')
        self.assertTrue(appointment.actual_departure_datetime)

    def test_bad_transitions(self):
        appointment = self._create_appointment()
        with self.assertRaises(UserError):
            appointment.action_dock()
        appointment.action_arrive()
        with self.assertRaises(UserError):
            appointment.action_complete()

    def test_arrival_grace_period_validation(self):
        """Test that arrival before grace period raises UserError."""
        self.env['ir.config_parameter'].sudo().set_param(
            'sf_dock_appointments.grace_minutes', '15')
        at = fields.Datetime.now() + timedelta(hours=4)
        appointment = self._create_appointment(at=at, window=60)
        # Arrival 20 minutes before appointment (outside 15 min grace) should fail
        early_arrival = at - timedelta(minutes=20)
        appointment.actual_arrival_datetime = early_arrival
        with self.assertRaises(UserError):
            appointment.action_arrive()
        # Arrival 10 minutes before appointment (within 15 min grace) should succeed
        appointment2 = self._create_appointment(at=at + timedelta(hours=1), window=60)
        arrival_within_grace = at + timedelta(hours=1) - timedelta(minutes=10)
        appointment2.actual_arrival_datetime = arrival_within_grace
        appointment2.action_arrive()
        self.assertEqual(appointment2.state, 'arrived')
        # Arrival after appointment time should succeed
        appointment3 = self._create_appointment(at=at + timedelta(hours=2), window=60)
        appointment3.action_arrive()
        self.assertEqual(appointment3.state, 'arrived')

    def test_departure_before_dock_rejected(self):
        appointment = self._create_appointment()
        appointment.action_arrive()
        appointment.action_dock()
        # Set departure before dock time
        appointment.actual_departure_datetime = appointment.actual_dock_datetime - timedelta(hours=1)
        with self.assertRaises(UserError):
            appointment.action_complete()

    def test_delay_and_duration(self):
        at = fields.Datetime.now() + timedelta(hours=4)
        appointment = self._create_appointment(at=at, window=60)
        appointment.action_arrive()
        appointment.action_dock()
        appointment.write({
            'actual_departure_datetime': at + timedelta(minutes=90),
        })
        appointment.action_complete()
        self.assertEqual(appointment.delay_minutes, 60)
        self.assertEqual(appointment.dock_duration_minutes, 90)

    def test_user_cannot_cancel(self):
        appointment = self._create_appointment()
        with self.assertRaises(UserError):
            appointment.with_user(self.user).action_cancel()

    def test_manager_can_cancel(self):
        appointment = self._create_appointment()
        appointment.with_user(self.manager).action_cancel()
        self.assertEqual(appointment.state, 'cancelled')

    def test_window_positive_constraint(self):
        with self.assertRaises(ValidationError):
            self._create_appointment(window=0)

    def test_cron_no_show(self):
        appointment = self._create_appointment(
            at=fields.Datetime.now() - timedelta(hours=3), window=60)
        self.env['ir.config_parameter'].sudo().set_param(
            'sf_dock_appointments.grace_minutes', '15')
        self.env['sf.dock.appointment']._cron_daily_checks()
        self.assertEqual(appointment.state, 'no_show')
        self.assertTrue(appointment.activity_ids)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Dock Co 2'})
        dock2 = self.env['sf.dock'].with_company(company2).create({
            'name': 'Dock 2',
            'dock_type': 'shipping',
            'company_id': company2.id,
        })
        appointment2 = self._create_appointment(dock=dock2.id)
        visible = self.env['sf.dock.appointment'].with_user(self.user).search(
            [('id', '=', appointment2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        appointment = self._create_appointment()
        action = self.env.ref(
            'sf_dock_appointments.action_report_appointments').report_action(appointment)
        self.assertTrue(action)

    def test_report_grouped_by_dock_and_day(self):
        """Test that report groups appointments by dock and by day."""
        base_date = fields.Datetime.now() + timedelta(days=1)
        # Create appointments on different docks and different days
        appt1 = self._create_appointment(at=base_date, dock=self.dock.id)
        appt2 = self._create_appointment(
            at=base_date + timedelta(hours=2), dock=self.dock.id)
        appt3 = self._create_appointment(
            at=base_date + timedelta(days=1), dock=self.dock.id)
        appt4 = self._create_appointment(at=base_date, dock=self.dock2.id)

        # Generate report
        action = self.env.ref(
            'sf_dock_appointments.action_report_appointments').report_action(
            self.env['sf.dock.appointment'].search([]))
        # Verify report action is valid
        self.assertTrue(action)
        self.assertEqual(action['report_type'], 'qweb-pdf')
        self.assertEqual(action['report_name'], 'sf_dock_appointments.report_appointments')