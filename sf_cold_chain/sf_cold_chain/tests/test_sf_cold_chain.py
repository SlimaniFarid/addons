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
            'device_type': 'cold_room',
            'target_min_temp': 2.0,
            'target_max_temp': 8.0,
        })
        self.carrier = self.env['res.partner'].create({
            'name': 'Carrier %s' % uuid.uuid4().hex[:6],
        })
        self.trip = self.env['sf.cold.trip'].create({
            'name': 'Trip 1',
            'origin': 'Warehouse A',
            'destination': 'Client B',
            'vehicle_plate': 'ABC-123',
            'driver_name': 'John Driver',
            'target_min_temp': -20.0,
            'target_max_temp': -15.0,
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

    def _create_reading(self, temperature, trip=None, site=None, at=None, source='manual'):
        vals = {
            'temperature': temperature,
            'recorded_at': at or fields.Datetime.now(),
            'source': source,
        }
        if trip:
            vals['trip_id'] = trip.id
        if site:
            vals['site_id'] = site.id
        return self.env['sf.cold.reading'].create(vals)

    def test_sequences(self):
        site = self.env['sf.cold.site'].create({
            'name': 'Freezer 2',
            'device_type': 'freezer',
            'target_min_temp': -25.0,
            'target_max_temp': -18.0,
        })
        self.assertTrue(site.name.startswith('CCS-'))
        trip = self.env['sf.cold.trip'].create({
            'origin': 'A',
            'destination': 'B',
            'target_min_temp': -20.0,
            'target_max_temp': -15.0,
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
        self.assertEqual(r2.excursion_id.max_temp, 13.0)
        self.assertEqual(r2.excursion_id.min_temp, 12.0)

    def test_excursion_severity_percentage(self):
        # Range: 2.0 to 8.0 = span of 6.0
        # 10% of range = 0.6, 20% = 1.2
        # Deviation of 1.0 (at 9.0) = 16.67% -> major
        # Deviation of 1.5 (at 9.5) = 25% -> critical
        r1 = self._create_reading(9.0, site=self.site)  # deviation 1.0 = 16.67% -> major
        self.assertEqual(r1.excursion_id.severity, 'major')
        r2 = self._create_reading(9.5, site=self.site)  # deviation 1.5 = 25% -> critical
        self.assertEqual(r2.excursion_id.severity, 'critical')
        # Test minor: deviation 0.3 (at 8.3) = 5% -> minor
        site2 = self.env['sf.cold.site'].create({
            'name': 'Site 2',
            'device_type': 'fridge',
            'target_min_temp': 0.0,
            'target_max_temp': 10.0,
        })
        r3 = self._create_reading(10.3, site=site2)  # deviation 0.3 = 3% -> minor
        self.assertEqual(r3.excursion_id.severity, 'minor')

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
                'target_min_temp': 8.0,
                'target_max_temp': 2.0,
            })

    def test_trip_temperature_range_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['sf.cold.trip'].create({
                'origin': 'A',
                'destination': 'B',
                'target_min_temp': 8.0,
                'target_max_temp': 2.0,
            })

    def test_trip_arrival_before_departure_constraint(self):
        with self.assertRaises(ValidationError):
            self.env['sf.cold.trip'].create({
                'origin': 'A',
                'destination': 'B',
                'target_min_temp': 2.0,
                'target_max_temp': 8.0,
                'departure_datetime': fields.Datetime.now(),
                'arrival_datetime': fields.Datetime.now() - timedelta(hours=1),
            })

    def test_site_state_computed(self):
        self.assertEqual(self.site.state, 'monitored')
        self._create_reading(12.0, site=self.site)
        self.assertEqual(self.site.state, 'out_of_range')

    def test_reading_source_field(self):
        r1 = self._create_reading(5.0, site=self.site, source='manual')
        self.assertEqual(r1.source, 'manual')
        r2 = self._create_reading(5.0, site=self.site, source='logger')
        self.assertEqual(r2.source, 'logger')

    def test_trip_workflow(self):
        self.trip.action_start()
        self.assertEqual(self.trip.state, 'in_transit')
        self.assertTrue(self.trip.departure_datetime)
        self.trip.action_complete()
        self.assertEqual(self.trip.state, 'completed')
        self.assertTrue(self.trip.arrival_datetime)

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
        self.assertTrue(excursion.resolved_on)
        self.assertTrue(excursion.ended_at)
        self.assertTrue(excursion.duration_minutes >= 0)

    def test_excursion_duration_ongoing(self):
        """Test that open excursion shows ongoing duration."""
        old_time = fields.Datetime.now() - timedelta(hours=2)
        reading = self._create_reading(12.0, site=self.site, at=old_time)
        excursion = reading.excursion_id
        # Duration should be > 0 (ongoing)
        self.assertTrue(excursion.duration_minutes > 100)  # ~120 minutes

    def test_excursion_min_max_temp(self):
        r1 = self._create_reading(12.0, site=self.site)
        r2 = self._create_reading(14.0, site=self.site)
        r3 = self._create_reading(11.0, site=self.site)
        excursion = r3.excursion_id
        self.assertEqual(excursion.min_temp, 11.0)
        self.assertEqual(excursion.max_temp, 14.0)

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
            'device_type': 'freezer',
            'target_min_temp': -10.0,
            'target_max_temp': 0.0,
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

    def test_report_wizard_from_site(self):
        """Test report wizard pre-filled from site."""
        self._create_reading(5.0, site=self.site)
        self._create_reading(12.0, site=self.site)
        wizard = self.env['sf.cold.chain.report.wizard'].create({
            'site_id': self.site.id,
        })
        action = wizard.action_print_report()
        self.assertTrue(action)
        self.assertEqual(action['res_model'], 'sf.cold.reading')

    def test_report_wizard_from_trip(self):
        """Test report wizard pre-filled from trip."""
        self._create_reading(-16.0, trip=self.trip)
        wizard = self.env['sf.cold.chain.report.wizard'].create({
            'trip_id': self.trip.id,
        })
        action = wizard.action_print_report()
        self.assertTrue(action)