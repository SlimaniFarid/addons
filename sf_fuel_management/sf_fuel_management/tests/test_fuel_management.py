# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestFuelManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Vehicle = self.env['sf.fuel.vehicle']
        self.Card = self.env['sf.fuel.card']
        self.Fill = self.env['sf.fuel.fill']
        self.Tank = self.env['sf.fuel.tank']
        self.Receipt = self.env['sf.fuel.tank.receipt']
        self.group_manager = self.env.ref(
            'sf_fuel_management.group_fuel_manager')
        self.group_user = self.env.ref(
            'sf_fuel_management.group_fuel_user')
        self.env.user.groups_id |= self.group_manager
        self.vehicle = self.Vehicle.create({
            'license_plate': 'AB-123-CD',
            'brand': 'Renault',
            'model': 'Master',
            'fuel_type': 'diesel',
        })
        self.card = self.Card.create({
            'card_number': 'FUE-0001',
            'vehicle_id': self.vehicle.id,
            'expiry_date': date.today() + timedelta(days=120),
        })
        self.tank = self.Tank.create({
            'site': 'Main Depot',
            'fuel_type': 'diesel',
            'capacity': 10000.0,
        })

    def _create_fill(self, odometer, liters, price=1.5):
        return self.Fill.create({
            'vehicle_id': self.vehicle.id,
            'card_id': self.card.id,
            'fill_date': date.today(),
            'odometer': odometer,
            'liters': liters,
            'price_per_liter': price,
            'supplier': 'Total',
        })

    def test_create_records_with_sequence(self):
        self.assertTrue(self.vehicle.name.startswith('VEH-'))
        self.assertTrue(self.card.name.startswith('CRD-'))
        self.assertTrue(self.tank.name.startswith('TNK-'))
        fill = self._create_fill(1000.0, 40.0)
        self.assertTrue(fill.name.startswith('FUL-'))
        receipt = self.Receipt.create({
            'tank_id': self.tank.id,
            'receipt_date': date.today(),
            'liters': 5000.0,
            'unit_price': 1.45,
            'supplier': 'DHL',
        })
        self.assertTrue(receipt.name.startswith('RCP-'))

    def test_total_computed(self):
        fill = self._create_fill(1000.0, 40.0, price=1.5)
        self.assertAlmostEqual(fill.total, 60.0, places=2)
        receipt = self.Receipt.create({
            'tank_id': self.tank.id,
            'receipt_date': date.today(),
            'liters': 1000.0,
            'unit_price': 1.45,
        })
        self.assertAlmostEqual(receipt.total, 1450.0, places=2)

    def test_consumption_calculation(self):
        self._create_fill(1000.0, 40.0)
        fill = self._create_fill(1100.0, 44.0)
        self.assertAlmostEqual(fill.previous_odometer, 1000.0, places=2)
        self.assertAlmostEqual(fill.consumption, 44.0, places=2)

    def test_no_previous_odometer(self):
        fill = self._create_fill(1000.0, 40.0)
        self.assertFalse(fill.previous_odometer)
        self.assertFalse(fill.consumption)

    def test_abnormal_consumption_alert_cron(self):
        self._create_fill(1000.0, 40.0)
        fill = self._create_fill(1100.0, 50.0)
        self.env.company.sf_fuel_max_l100 = 12.0
        self.Fill._check_fuel_alerts()
        self.assertTrue(fill.activity_ids)
        count = len(fill.activity_ids)
        self.Fill._check_fuel_alerts()
        self.assertEqual(len(fill.activity_ids), count)

    def test_card_expiry_alert_cron(self):
        card = self.Card.create({
            'card_number': 'FUE-0002',
            'vehicle_id': self.vehicle.id,
            'expiry_date': date.today() + timedelta(days=3),
        })
        self.env.company.sf_fuel_alert_days = 7
        self.Fill._check_fuel_alerts()
        self.assertTrue(card.activity_ids)

    def test_blocked_card_cannot_be_used(self):
        self.card.action_block()
        with self.assertRaises(UserError):
            self._create_fill(1200.0, 10.0)

    def test_expired_card_cannot_be_used(self):
        self.card.action_expire()
        with self.assertRaises(UserError):
            self._create_fill(1200.0, 10.0)

    def test_fill_workflow(self):
        fill = self._create_fill(1000.0, 40.0)
        fill.action_record()
        self.assertEqual(fill.state, 'recorded')
        fill.action_done()
        self.assertEqual(fill.state, 'done')

    def test_card_block_manager_only(self):
        user = self.env['res.users'].create({
            'name': 'Fuel User',
            'login': 'fuel_user',
            'groups_id': [(4, self.group_user.id)],
        })
        with self.assertRaises(UserError):
            self.Card.with_user(user).browse(self.card.id).action_block()

    def test_fill_record_manager_only(self):
        user = self.env['res.users'].create({
            'name': 'Fuel User 2',
            'login': 'fuel_user_2',
            'groups_id': [(4, self.group_user.id)],
        })
        fill = self._create_fill(1000.0, 40.0)
        with self.assertRaises(UserError):
            fill.with_user(user).action_record()

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Fuel Company B'})
        user = self.env['res.users'].create({
            'name': 'Fuel Company A User',
            'login': 'fuel_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        other = self.Vehicle.with_company(company_b).create({
            'license_plate': 'XY-456-ZZ',
            'brand': 'Volvo',
            'model': 'FH',
            'fuel_type': 'diesel',
        })
        self.assertNotIn(other, self.Vehicle.with_user(user).search(
            [('id', '=', other.id)]))

    def test_report_records_exist(self):
        reports = self.env['ir.actions.report'].search([
            ('report_name', 'in', [
                'sf_fuel_management.report_monthly_consumption_template',
                'sf_fuel_management.report_tank_monitoring_template',
            ]),
        ])
        self.assertEqual(len(reports), 2)