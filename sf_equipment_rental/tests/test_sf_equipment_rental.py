# -*- coding: utf-8 -*-
import uuid

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfEquipmentRental(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })
        self.income_account = self.env['account.account'].create({
            'name': 'Test Income',
            'account_type': 'income',
            'code': 'TESTINC',
            'company_id': self.env.company.id,
        })
        self.sale_journal = self.env['account.journal'].create({
            'name': 'Test Sales',
            'type': 'sale',
            'code': 'TSALE',
            'company_id': self.env.company.id,
        })
        self.category = self.env['sf.rental.category'].create({})
        self.equipment = self.env['sf.rental.equipment'].create({
            'category_id': self.category.id,
            'hourly_price': 100.0,
            'daily_price': 800.0,
            'weekly_price': 4000.0,
            'monthly_price': 14000.0,
        })

    def _create_contract(self, days=2, state='draft'):
        from datetime import datetime, timedelta
        start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        contract = self.env['sf.rental.contract'].create({
            'partner_id': self.customer.id,
            'start_datetime': start,
            'end_datetime': start + timedelta(days=days),
            'state': state,
        })
        self.env['sf.rental.contract.line'].create({
            'contract_id': contract.id,
            'equipment_id': self.equipment.id,
            'qty': 1,
        })
        return contract

    def test_sequences(self):
        self.assertTrue(self.equipment.name.startswith('EQP-'))
        self.assertTrue(self.category.name.startswith('CAT-'))
        contract = self._create_contract()
        self.assertTrue(contract.name.startswith('RTL-'))

    def test_daily_tier_price(self):
        contract = self._create_contract(days=2)
        line = contract.line_ids[0]
        self.assertEqual(line.price_unit, 1600.0)
        self.assertEqual(line.subtotal, 1600.0)

    def test_weekly_tier_price(self):
        contract = self._create_contract(days=9)
        line = contract.line_ids[0]
        self.assertEqual(line.price_unit, 8000.0)

    def test_monthly_tier_price(self):
        contract = self._create_contract(days=32)
        line = contract.line_ids[0]
        self.assertEqual(line.price_unit, 14000.0)

    def test_hourly_tier_price(self):
        from datetime import datetime, timedelta
        start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        contract = self.env['sf.rental.contract'].create({
            'partner_id': self.customer.id,
            'start_datetime': start,
            'end_datetime': start + timedelta(hours=4),
        })
        self.env['sf.rental.contract.line'].create({
            'contract_id': contract.id,
            'equipment_id': self.equipment.id,
            'qty': 1,
        })
        self.assertEqual(contract.line_ids[0].price_unit, 400.0)

    def test_tier_boundaries(self):
        from datetime import datetime, timedelta
        start = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        def price(duration):
            contract = self.env['sf.rental.contract'].create({
                'partner_id': self.customer.id,
                'start_datetime': start,
                'end_datetime': start + duration,
            })
            self.env['sf.rental.contract.line'].create({
                'contract_id': contract.id,
                'equipment_id': self.equipment.id,
                'qty': 1,
            })
            return contract.line_ids[0].price_unit
        self.assertEqual(price(timedelta(hours=24)), 800.0)
        self.assertEqual(price(timedelta(days=7)), 4000.0)
        self.assertEqual(price(timedelta(days=30)), 20000.0)
        self.assertEqual(price(timedelta(days=31)), 14000.0)

    def test_contract_workflow(self):
        contract = self._create_contract()
        contract.action_confirm()
        self.assertEqual(contract.state, 'confirmed')
        contract.action_active()
        self.assertEqual(contract.state, 'active')
        self.assertEqual(self.equipment.state, 'out')
        self.assertTrue(contract.inspection_out_ids)
        self.env['sf.rental.inspection'].create({
            'contract_id': contract.id,
            'line_id': contract.line_ids[0].id,
            'direction': 'in',
            'condition': 'good',
        }).action_done()
        contract.action_return()
        self.assertEqual(contract.state, 'returned')
        self.assertEqual(self.equipment.state, 'available')
        contract.action_invoice()
        self.assertEqual(contract.state, 'invoiced')
        self.assertTrue(contract.invoice_id)
        contract.action_close()
        self.assertEqual(contract.state, 'closed')

    def test_conflict_detection(self):
        contract1 = self._create_contract(days=3)
        contract1.action_confirm()
        contract2 = self._create_contract(days=1)
        with self.assertRaises(UserError):
            contract2.action_confirm()

    def test_return_requires_in_inspection(self):
        contract = self._create_contract()
        contract.action_confirm()
        contract.action_active()
        with self.assertRaises(UserError):
            contract.action_return()

    def test_damage_penalty(self):
        contract = self._create_contract()
        contract.action_confirm()
        contract.action_active()
        inspection = self.env['sf.rental.inspection'].create({
            'contract_id': contract.id,
            'line_id': contract.line_ids[0].id,
            'direction': 'in',
            'condition': 'damaged',
        })
        self.env['sf.rental.damage'].create({
            'inspection_id': inspection.id,
            'description': 'Scratched',
            'penalty_amount': 200.0,
        })
        inspection.action_done()
        contract.action_return()
        contract.action_invoice()
        self.assertEqual(contract.penalty_total, 200.0)

    def test_damaged_requires_damage_record(self):
        contract = self._create_contract()
        contract.action_confirm()
        contract.action_active()
        inspection = self.env['sf.rental.inspection'].create({
            'contract_id': contract.id,
            'line_id': contract.line_ids[0].id,
            'direction': 'in',
            'condition': 'broken',
        })
        with self.assertRaises(UserError):
            inspection.action_done()

    def test_maintenance_blocks_rental(self):
        from datetime import date, timedelta
        maintenance = self.env['sf.rental.maintenance'].create({
            'equipment_id': self.equipment.id,
            'scheduled_date': date.today() + timedelta(days=5),
        })
        maintenance.action_schedule()
        self.assertEqual(maintenance.state, 'scheduled')
        self.assertEqual(self.equipment.state, 'maintenance')
        contract = self._create_contract()
        contract.action_confirm()
        with self.assertRaises(UserError):
            contract.action_active()

    def test_cancel_active_impossible(self):
        contract = self._create_contract()
        contract.action_confirm()
        contract.action_active()
        with self.assertRaises(UserError):
            contract.action_cancel()

    def test_report_generation(self):
        contract = self._create_contract()
        contract.action_confirm()
        contract.action_active()
        inspection = contract.inspection_out_ids[0]
        for report in ['action_report_rental_contract', 'action_report_fleet']:
            record = contract if report == 'action_report_rental_contract' else self.equipment
            action = self.env.ref('sf_equipment_rental.%s' % report).report_action(record)
            self.assertTrue(action)
        action = self.env.ref('sf_equipment_rental.action_report_out_in_ticket').report_action(inspection)
        self.assertTrue(action)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Second Co'})
        contract1 = self._create_contract()
        contract2 = self.env['sf.rental.contract'].with_company(company2).create({
            'partner_id': self.customer.id,
            'start_datetime': contract1.start_datetime,
            'end_datetime': contract1.end_datetime,
            'company_id': company2.id,
        })
        user = self.env['res.users'].create({
            'name': 'User 1',
            'login': 'user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref('sf_equipment_rental.group_sf_rental_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
        })
        self.assertTrue(contract1.with_user(user).exists())
        self.assertFalse(contract2.with_user(user).exists())