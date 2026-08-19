# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo import fields
from odoo.exceptions import UserError


class TestEnergyMonitoring(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Site = self.env['sf.energy.site']
        self.Meter = self.env['sf.energy.meter']
        self.Reading = self.env['sf.energy.reading']
        self.Objective = self.env['sf.energy.objective']
        self.manager = self.env['res.users'].create({
            'name': 'Energy Manager',
            'login': 'energy_manager_test',
            'groups_id': [
                (6, 0, [
                    self.env.ref('sf_energy_monitoring.group_energy_manager').id,
                ]),
            ],
        })

        self.site = self.Site.create({'name': 'HQ Building'})
        self.meter = self.Meter.create({
            'name': 'Main Electricity Meter',
            'site_id': self.site.id,
            'utility_type': 'electricity',
            'price_unit': 0.95,
        })

    def _reading(self, date, index, **kw):
        vals = {
            'meter_id': self.meter.id,
            'date': date,
            'index_value': index,
        }
        vals.update(kw)
        return self.Reading.create(vals)

    def test_01_site_and_meter_creation(self):
        self.assertEqual(self.site.name, 'HQ Building')
        self.assertEqual(self.meter.site_id.id, self.site.id)
        self.assertEqual(self.meter.utility_type, 'electricity')
        self.assertEqual(self.meter.unit, 'kwh')
        self.assertEqual(self.meter.state, 'active')

    def test_02_first_reading_consumption_equals_index(self):
        reading = self._reading('2026-01-15', 1000.0)
        self.assertEqual(reading.consumption, 1000.0)
        self.assertEqual(reading.state, 'draft')

    def test_03_consumption_between_two_indexes(self):
        first = self._reading('2026-01-15', 1000.0)
        first.action_confirm()
        second = self._reading('2026-02-15', 1250.0)
        self.assertEqual(second.consumption, 250.0)
        self.assertAlmostEqual(second.cost, 237.5, places=2)

    def test_04_cost_uses_price_unit(self):
        first = self._reading('2026-01-15', 1000.0)
        first.action_confirm()
        second = self._reading('2026-02-15', 1250.0)
        self.assertAlmostEqual(second.cost, 250.0 * 0.95, places=2)

    def test_05_decreasing_index_rejected(self):
        first = self._reading('2026-01-15', 1000.0)
        first.action_confirm()
        with self.assertRaises(UserError):
            self._reading('2026-02-15', 900.0)

    def test_06_meter_reset_allows_lower_index(self):
        first = self._reading('2026-01-15', 1000.0)
        first.action_confirm()
        second = self._reading('2026-02-15', 500.0, meter_reset=True)
        self.assertEqual(second.consumption, 500.0)

    def test_07_duplicate_date_rejected(self):
        self._reading('2026-01-15', 1000.0)
        with self.assertRaises(UserError):
            self._reading('2026-01-15', 1100.0)

    def test_08_confirm_workflow(self):
        reading = self._reading('2026-01-15', 1000.0)
        reading.with_user(self.manager).action_confirm()
        self.assertEqual(reading.state, 'confirmed')
        self.assertTrue(reading.confirmed_by)
        reading.action_to_draft()
        self.assertEqual(reading.state, 'draft')

    def test_09_confirmed_reading_cannot_be_modified(self):
        reading = self._reading('2026-01-15', 1000.0)
        reading.with_user(self.manager).action_confirm()
        with self.assertRaises(UserError):
            reading.write({'index_value': 1200.0})

    def test_10_meter_last_reading_computed(self):
        first = self._reading('2026-01-15', 1000.0)
        first.action_confirm()
        self.meter.invalidate_model(['last_reading_date', 'last_index'])
        self.assertEqual(self.meter.last_reading_date,
                         first.date)
        self.assertEqual(self.meter.last_index, 1000.0)

    def test_11_objective_creation(self):
        objective = self.Objective.create({
            'site_id': self.site.id,
            'utility_type': 'electricity',
            'year': 2026,
            'target_amount': 500.0,
            'period': 'month',
        })
        self.assertEqual(objective.state, 'active')
        self.assertEqual(objective.year, 2026)

    def test_12_objective_invalid_target_rejected(self):
        with self.assertRaises(UserError):
            self.Objective.create({
                'site_id': self.site.id,
                'utility_type': 'electricity',
                'year': 2026,
                'target_amount': -10.0,
            })

    def test_13_objective_close(self):
        objective = self.Objective.create({
            'site_id': self.site.id,
            'utility_type': 'electricity',
            'year': 2026,
            'target_amount': 500.0,
            'period': 'month',
        })
        objective.action_close()
        self.assertEqual(objective.state, 'expired')

    def test_14_period_consumption_summary(self):
        first = self._reading('2026-01-15', 1000.0)
        first.action_confirm()
        second = self._reading('2026-02-15', 1250.0)
        second.action_confirm()
        from datetime import date
        objective = self.Objective.create({
            'site_id': self.site.id,
            'utility_type': 'electricity',
            'year': 2026,
            'target_amount': 500.0,
            'period': 'year',
        })
        consumption = objective._get_period_consumption(
            date(2026, 1, 1), date(2026, 12, 31))
        self.assertEqual(consumption, 1250.0)

    def test_15_objective_breach_schedules_activity(self):
        objective = self.Objective.create({
            'site_id': self.site.id,
            'utility_type': 'electricity',
            'year': 2026,
            'target_amount': 100.0,
            'period': 'month',
        })
        reading = self._reading(fields.Date.today().strftime('%Y-%m-%d'),
                                5000.0)
        reading.action_confirm()
        objective.with_user(self.manager)._check_objective_breach()
        activities = objective.activity_ids
        self.assertTrue(activities)