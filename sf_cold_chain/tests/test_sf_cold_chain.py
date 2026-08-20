# -*- coding: utf-8 -*-
import uuid
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfColdChain(TransactionCase):

    def setUp(self):
        super().setUp()
        self.site = self.env['sf.cold.site'].create({
            'name': 'Warehouse Cold Room',
            'site_type': 'cold_room',
            'temperature_min': 2.0,
            'temperature_max': 8.0,
        })
        self.carrier = self.env['res.partner'].create({
            'name': 'Carrier %s' % uuid.uuid4().hex[:6],
        })
        self.trip = self.env['sf.cold.trip'].create({
            'name': 'Trip 1',
            'carrier_id': self.carrier.id,
            'temperature_min': -20.0,
            'temperature_max': -15.0,
        })
        self.manager_group = self.env.ref(
            'sf_cold_chain.group_sf_cold_chain_manager')
        self.user_group = self.env.ref(
            'sf_cold_chain.group_sf_cold_chain_user')
        self.manager = self.env['res.users'].create({
            'name': 'Cold Chain Manager',
            'login': 'cold_mgr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.manager_group.id])],
        })
        self.user = self.env['res.users'].create({
            'name': 'Cold Chain User',
            'login': 'cold_usr_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.user_group.id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })

    def _create_reading(self, temperature, trip=None, site=None, at=None):
        vals = {
            'temperature': temperature,
            'reading_datetime': at or fields.Datetime.now(),
        }
        if trip:
            vals['trip_id'] = trip.id
        if site:
            vals['site_id'] = site.id
        return self.env['sf.cold.reading'].create(vals)

    def test_sequences(self):
        site = self.env['sf.cold.site'].create({
            'name': 'Freezer 2',
            'site_type': 'freezer',
            'temperature_min': -25.0,
            'temperature_max': -18.0,
        })
        self.assertTrue(site.name.startswith('CCS-'))
        trip = self.env['sf.cold.trip'].create({
            'carrier_id': self.carrier.id,
            'temperature_min': -20.0,
            'temperature_max': -15.0,
        })
        self.assertTrue(trip.name.startswith('CPT-'))

    def test_reading_in_range(self):
        reading = self._create_reading(5.0, site=self.site)
        self.assertTrue(reading.within_range)
        self.assertEqual(reading.deviation, 0.0)
        self.assertFalse(reading.excursion_id)

    def test_reading_out_of_range_creates_excursion(self):
        reading = self._create_reading(12.0, site=self.site)
        self.assertFalse(reading.within_range)
        self.assertEqual(reading.deviation, 4.0)
        self.assertTrue(reading.excursion_id)
        self.assertEqual(reading.excursion_id.state, 'open')

    def test_reading_out_of_range_reuses_excursion(self):
        r1 = self._create_reading(12.0, site=self.site)
        r2 = self._create_reading(13.0, site=self.site)
        self.assertEqual(r1.excursion_id, r2.excursion_id)
        self.assertEqual(r2.excursion_id.max_deviation, 5.0)
        self.assertEqual(r2.excursion_id.severity, 'high')

    def test_excursion_severity(self):
        r1 = self._create_reading(9.0, site=self.site)
        self.assertEqual(r1.excursion_id.max_deviation, 1.0)
        self.assertEqual(r1.excursion_id.severity, 'low')
        r2 = self._create_reading(11.0, site=self.site)
        self.assertEqual(r2.excursion_id.max_deviation, 3.0)
        self.assertEqual(r2.excursion_id.severity, 'medium')

    def test_trip_reading_limits(self):
        reading = self._create_reading(-16.0, trip=self.trip)
        self.assertTrue(reading.within_range)
        self.assertEqual(reading.temperature_min, -20.0)
        self.assertEqual(reading.temperature_max, -15.0)

    def test_reading_requires_source(self):
        with self.assertRaises(ValidationError):
            self._create_reading(5.0)

    def test_site_temperature_range_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['sf.cold.site'].create({
                'name': 'Bad Site',
                'temperature_min': 8.0,
                'temperature_max': 2.0,
            })

    def test_trip_workflow(self):
        self.trip.action_start()
        self.assertEqual(self.trip.state, 'in_transit')
        self.assertTrue(self.trip.actual_departure)
        self.trip.action_complete()
        self.assertEqual(self.trip.state, 'completed')
        self.assertTrue(self.trip.actual_arrival)

    def test_trip_bad_transition(self):
        with self.assertRaises(UserError):
            self.trip.action_complete()

    def test_user_cannot_cancel_trip(self):
        with self.assertRaises(UserError):
            self.trip.with_user(self.user).action_cancel()

    def test_manager_can_cancel_trip(self):
        self.trip.with_user(self.manager).action_cancel()
        self.assertEqual(self.trip.state, 'cancelled')

    def test_resolve_requires_manager(self):
        reading = self._create_reading(12.0, site=self.site)
        excursion = reading.excursion_id
        with self.assertRaises(UserError):
            excursion.with_user(self.user).action_resolve()

    def test_resolve(self):
        reading = self._create_reading(12.0, site=self.site)
        excursion = reading.excursion_id
        excursion.with_user(self.manager).action_resolve()
        self.assertEqual(excursion.state, 'resolved')
        self.assertTrue(excursion.resolved_by)
        self.assertTrue(excursion.resolved_datetime)
        self.assertTrue(excursion.duration_minutes >= 0)

    def test_cron_escalation(self):
        self.env['ir.config_parameter'].sudo().set_param(
            'sf_cold_chain.alert_hours', '24')
        old = self._create_reading(
            12.0, site=self.site,
            at=fields.Datetime.now() - timedelta(hours=30))
        fresh = self._create_reading(
            12.0, site=self.site, at=fields.Datetime.now())
        self.env['sf.cold.excursion']._cron_escalation()
        self.assertTrue(old.excursion_id.activity_ids)
        self.assertFalse(fresh.excursion_id.activity_ids)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Cold Co 2'})
        site2 = self.env['sf.cold.site'].with_company(company2).create({
            'name': 'Site 2',
            'temperature_min': -10.0,
            'temperature_max': 0.0,
            'company_id': company2.id,
        })
        reading2 = self._create_reading(5.0, site=site2)
        visible = self.env['sf.cold.reading'].with_user(self.user).search(
            [('id', '=', reading2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        reading = self._create_reading(5.0, site=self.site)
        action = self.env.ref(
            'sf_cold_chain.action_report_cold_log').report_action(reading)
        self.assertTrue(action)