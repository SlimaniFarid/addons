# -*- coding: utf-8 -*-
import uuid
from datetime import date, timedelta

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfUtilityBilling(TransactionCase):

    def setUp(self):
        super().setUp()
        self.env.user.groups_id += self.env.ref('sf_utility_billing.group_sf_utility_manager')
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })
        self.meter = self.env['sf.utility.meter'].create({
            'partner_id': self.customer.id,
            'utility_type': 'water',
            'opening_index': 100.0,
        })
        today = date.today()
        self.campaign = self.env['sf.utility.campaign'].create({
            'period_start': today - timedelta(days=30),
            'period_end': today,
            'meter_ids': [(6, 0, self.meter.ids)],
        })
        self.campaign.action_open()

    def _create_company(self):
        return self.env['res.company'].create({
            'name': 'Company %s' % uuid.uuid4().hex[:6],
        })

    def _create_user(self, company_ids, manager=False):
        groups = [
            self.env.ref('base.group_user'),
            self.env.ref('sf_utility_billing.group_sf_utility_user'),
        ]
        if manager:
            groups.append(self.env.ref('sf_utility_billing.group_sf_utility_manager'))
        return self.env['res.users'].create({
            'name': 'User %s' % uuid.uuid4().hex[:6],
            'login': 'user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [g.id for g in groups])],
            'company_ids': [(6, 0, company_ids)],
            'company_id': company_ids[0],
        })

    def _open_second_campaign(self):
        camp2 = self.env['sf.utility.campaign'].create({
            'period_start': self.campaign.period_end + timedelta(days=1),
            'period_end': self.campaign.period_end + timedelta(days=30),
            'meter_ids': [(6, 0, self.meter.ids)],
        })
        camp2.action_open()
        return camp2

    def _create_tariff(self):
        tariff = self.env['sf.utility.tariff'].create({
            'name': 'Water Tariff',
            'utility_type': 'water',
            'effective_from': date.today() - timedelta(days=60),
            'line_ids': [
                (0, 0, {'from_quantity': 0.0, 'to_quantity': 10.0, 'price_per_unit': 1.0}),
                (0, 0, {'from_quantity': 10.0, 'to_quantity': 50.0, 'price_per_unit': 2.0}),
                (0, 0, {'from_quantity': 50.0, 'price_per_unit': 3.0}),
            ],
        })
        return tariff

    def test_sequences(self):
        self.assertTrue(self.meter.name.startswith('CTR-'))
        self.assertTrue(self.campaign.name.startswith('CMP-'))
        reading = self.campaign.reading_ids[:1]
        self.assertTrue(reading.name.startswith('REL-'))
        tariff = self._create_tariff()
        self.assertTrue(tariff.name.startswith('TRF-'))

    def test_campaign_opens_readings(self):
        self.assertEqual(self.campaign.state, 'open')
        self.assertEqual(len(self.campaign.reading_ids), 1)

    def test_consumption_calculation(self):
        reading = self.campaign.reading_ids[:1]
        reading.index = 130.0
        reading.action_done()
        reading.action_validate()
        self.assertEqual(reading.consumption, 30.0)

    def test_decreasing_index_rejected(self):
        reading = self.campaign.reading_ids[:1]
        reading.index = 90.0
        reading.action_done()
        with self.assertRaises(UserError):
            reading.action_validate()
        self.assertEqual(reading.state, 'rejected')

    def test_validated_reading_immutable(self):
        reading = self.campaign.reading_ids[:1]
        reading.index = 130.0
        reading.action_done()
        reading.action_validate()
        with self.assertRaises(UserError):
            reading.index = 140.0

    def test_tiered_amount(self):
        self._create_tariff()
        reading = self.campaign.reading_ids[:1]
        reading.index = 170.0
        reading.action_done()
        reading.action_validate()
        self.assertEqual(reading.consumption, 70.0)
        self.campaign.action_close()
        invoice = self.env['sf.utility.invoice'].search([('reading_id', '=', reading.id)])
        self.assertTrue(invoice)
        # 0-10 @1, 10-50 @2, 50-70 @3 => 10 + 80 + 60 = 150
        self.assertEqual(invoice.amount_total, 150.0)

    def test_campaign_close_requires_validated(self):
        reading = self.campaign.reading_ids[:1]
        reading.index = 120.0
        reading.action_done()
        with self.assertRaises(UserError):
            self.campaign.action_close()

    def test_invoice_posting_creates_move(self):
        self._create_tariff()
        reading = self.campaign.reading_ids[:1]
        reading.index = 130.0
        reading.action_done()
        reading.action_validate()
        self.campaign.action_close()
        invoice = self.env['sf.utility.invoice'].search([('reading_id', '=', reading.id)])
        invoice.action_post()
        self.assertEqual(invoice.state, 'posted')
        self.assertTrue(invoice.invoice_id)

    def test_anomaly_detection(self):
        threshold = float(self.env['ir.config_parameter'].sudo().get_param(
            'sf_utility_billing.anomaly_threshold', '500.0'))
        reading = self.campaign.reading_ids[:1]
        reading.index = self.meter.opening_index + threshold + 1.0
        reading.action_done()
        reading.action_validate()
        self.assertTrue(self.meter.activity_ids.filtered(
            lambda a: 'Abnormal consumption' in a.summary))

    def test_overdue_cron(self):
        self._create_tariff()
        reading = self.campaign.reading_ids[:1]
        reading.index = 130.0
        reading.action_done()
        reading.action_validate()
        self.campaign.action_close()
        invoice = self.env['sf.utility.invoice'].search([('reading_id', '=', reading.id)])
        invoice.action_post()
        invoice.invoice_id.invoice_date_due = date.today() - timedelta(days=1)
        invoice._cron_daily_checks()
        self.assertEqual(invoice.state, 'overdue')

    def test_report_generation(self):
        reading = self.campaign.reading_ids[:1]
        reading.index = 130.0
        reading.action_done()
        reading.action_validate()
        self._create_tariff()
        self.campaign.action_close()
        invoice = self.env['sf.utility.invoice'].search([('reading_id', '=', reading.id)])
        for report in ['action_report_reading', 'action_report_invoice', 'action_report_overdue']:
            action = self.env.ref('sf_utility_billing.%s' % report).report_action(reading)
            self.assertTrue(action)
        action = self.env.ref('sf_utility_billing.action_report_campaign').report_action(self.campaign)
        self.assertTrue(action)

    def test_rejected_reset(self):
        reading = self.campaign.reading_ids[:1]
        reading.index = 90.0
        reading.action_done()
        try:
            reading.action_validate()
        except UserError:
            pass
        self.assertEqual(reading.state, 'rejected')
        reading.index = 110.0
        reading.action_reset()
        self.assertEqual(reading.state, 'draft')
        reading.action_done()
        reading.action_validate()
        self.assertEqual(reading.state, 'validated')

    def test_consumption_uses_previous_validated(self):
        r1 = self.campaign.reading_ids[:1]
        r1.index = 130.0
        r1.action_done()
        r1.action_validate()
        self.assertEqual(r1.consumption, 30.0)
        camp2 = self._open_second_campaign()
        r2 = camp2.reading_ids[:1]
        r2.index = 200.0
        r2.action_done()
        r2.action_validate()
        self.assertEqual(r2.consumption, 70.0)

    def test_recompute_after_reject(self):
        r1 = self.campaign.reading_ids[:1]
        r1.index = 130.0
        r1.action_done()
        r1.action_validate()
        camp2 = self._open_second_campaign()
        r2 = camp2.reading_ids[:1]
        r2.index = 200.0
        r2.action_done()
        r2.action_validate()
        self.assertEqual(r2.consumption, 70.0)
        r1.action_reject()
        self.assertEqual(r2.consumption, 100.0)

    def test_backdated_reading_recompute(self):
        r1 = self.campaign.reading_ids[:1]
        r1.index = 130.0
        r1.action_done()
        r1.action_validate()
        camp2 = self._open_second_campaign()
        r0 = self.env['sf.utility.meter.reading'].create({
            'meter_id': self.meter.id,
            'campaign_id': camp2.id,
            'reading_date': self.campaign.period_start,
            'index': 180.0,
            'company_id': self.meter.company_id.id,
        })
        r0.action_done()
        r0.action_validate()
        self.assertEqual(r1.consumption, 130.0 - 180.0)

    def test_zero_index_not_falsy(self):
        reading = self.campaign.reading_ids[:1]
        reading.index = 0.0
        reading.action_done()
        with self.assertRaises(UserError):
            reading.action_validate()
        self.assertEqual(reading.state, 'rejected')

    def test_non_manager_cannot_reject_validated(self):
        r1 = self.campaign.reading_ids[:1]
        r1.index = 130.0
        r1.action_done()
        r1.action_validate()
        user = self._create_user([self.env.company.id])
        with self.assertRaises(UserError):
            user.env['sf.utility.meter.reading'].browse(r1.id).write({'state': 'rejected'})
        manager = self._create_user([self.env.company.id], manager=True)
        manager.env['sf.utility.meter.reading'].browse(r1.id).write({'state': 'rejected'})
        self.assertEqual(r1.state, 'rejected')

    def test_tariff_first_tier_nonzero(self):
        self.env['sf.utility.tariff'].create({
            'name': 'NonZero Start Tariff',
            'utility_type': 'water',
            'effective_from': date.today() - timedelta(days=60),
            'line_ids': [(0, 0, {
                'from_quantity': 100.0, 'to_quantity': 200.0, 'price_per_unit': 2.0})],
        })
        invoice = self.env['sf.utility.invoice'].create({
            'meter_id': self.meter.id,
            'campaign_id': self.campaign.id,
            'consumption': 50.0,
        })
        self.assertEqual(invoice.amount_total, 0.0)

    def test_tariff_empty_grid(self):
        self.env['sf.utility.tariff'].create({
            'name': 'Empty Tariff',
            'utility_type': 'water',
            'effective_from': date.today() - timedelta(days=60),
        })
        invoice = self.env['sf.utility.invoice'].create({
            'meter_id': self.meter.id,
            'campaign_id': self.campaign.id,
            'consumption': 50.0,
        })
        self.assertEqual(invoice.amount_total, 0.0)

    def test_tariff_contiguity_validation(self):
        with self.assertRaises(UserError):
            self.env['sf.utility.tariff'].create({
                'name': 'Gap Tariff',
                'utility_type': 'water',
                'effective_from': date.today() - timedelta(days=60),
                'line_ids': [
                    (0, 0, {'from_quantity': 0.0, 'to_quantity': 10.0, 'price_per_unit': 1.0}),
                    (0, 0, {'from_quantity': 20.0, 'to_quantity': 30.0, 'price_per_unit': 2.0}),
                ],
            })

    def test_zero_consumption_no_invoice(self):
        self._create_tariff()
        reading = self.campaign.reading_ids[:1]
        reading.index = 100.0
        reading.action_done()
        reading.action_validate()
        self.assertEqual(reading.consumption, 0.0)
        self.campaign.action_close()
        invoice = self.env['sf.utility.invoice'].search([('reading_id', '=', reading.id)])
        self.assertFalse(invoice)

    def test_campaign_period_validation(self):
        with self.assertRaises(UserError):
            self.env['sf.utility.campaign'].create({
                'period_start': date.today(),
                'period_end': date.today() - timedelta(days=1),
            })

    def test_campaign_cannot_cancel_closed(self):
        self._create_tariff()
        reading = self.campaign.reading_ids[:1]
        reading.index = 130.0
        reading.action_done()
        reading.action_validate()
        self.campaign.action_close()
        with self.assertRaises(UserError):
            self.campaign.action_cancel()

    def test_cancel_draft_invoice(self):
        self._create_tariff()
        reading = self.campaign.reading_ids[:1]
        reading.index = 130.0
        reading.action_done()
        reading.action_validate()
        self.campaign.action_close()
        invoice = self.env['sf.utility.invoice'].search([('reading_id', '=', reading.id)])
        invoice.action_cancel()
        self.assertEqual(invoice.state, 'cancelled')

    def test_cannot_cancel_paid_invoice(self):
        self._create_tariff()
        reading = self.campaign.reading_ids[:1]
        reading.index = 130.0
        reading.action_done()
        reading.action_validate()
        self.campaign.action_close()
        invoice = self.env['sf.utility.invoice'].search([('reading_id', '=', reading.id)])
        invoice.action_post()
        invoice.state = 'paid'
        with self.assertRaises(UserError):
            invoice.action_cancel()

    def test_import_wizard(self):
        meter2 = self.env['sf.utility.meter'].create({
            'partner_id': self.customer.id,
            'utility_type': 'water',
            'opening_index': 0.0,
        })
        self.campaign.meter_ids += meter2
        wizard = self.env['sf.utility.import.wizard'].create({
            'campaign_id': self.campaign.id,
            'data': '%s,135.0,2026-02-15\n%s,140.0,2026-02-20' % (self.meter.name, meter2.name),
        })
        wizard.action_import()
        r1 = self.campaign.reading_ids.filtered(lambda r: r.meter_id == self.meter)
        r2 = self.campaign.reading_ids.filtered(lambda r: r.meter_id == meter2)
        self.assertEqual(len(r1), 1)
        self.assertEqual(r1.index, 135.0)
        self.assertEqual(len(r2), 1)
        self.assertEqual(r2.index, 140.0)
        self.assertEqual(r2.company_id.id, meter2.company_id.id)

    def test_import_wizard_rejects_invalid(self):
        wizard = self.env['sf.utility.import.wizard'].create({
            'campaign_id': self.campaign.id,
            'data': 'unknown_meter,10.0',
        })
        with self.assertRaises(UserError):
            wizard.action_import()

    def test_multi_company_isolation(self):
        company_b = self._create_company()
        meter_b = self.env['sf.utility.meter'].create({
            'partner_id': self.customer.id,
            'utility_type': 'water',
            'company_id': company_b.id,
        })
        user_a = self._create_user([self.env.company.id])
        meters = user_a.env['sf.utility.meter'].search([])
        self.assertIn(self.meter.id, meters.ids)
        self.assertNotIn(meter_b.id, meters.ids)

    def test_manager_sees_all_companies(self):
        company_b = self._create_company()
        meter_b = self.env['sf.utility.meter'].create({
            'partner_id': self.customer.id,
            'utility_type': 'water',
            'company_id': company_b.id,
        })
        manager = self._create_user([self.env.company.id], manager=True)
        meters = manager.env['sf.utility.meter'].search([])
        self.assertIn(meter_b.id, meters.ids)

    def test_tariff_multi_company(self):
        company_b = self._create_company()
        self.env['sf.utility.tariff'].create({
            'name': 'Tariff Company B',
            'utility_type': 'water',
            'effective_from': date.today() - timedelta(days=60),
            'company_id': company_b.id,
            'line_ids': [(0, 0, {
                'from_quantity': 0.0, 'to_quantity': 10.0, 'price_per_unit': 9.0})],
        })
        invoice = self.env['sf.utility.invoice'].create({
            'meter_id': self.meter.id,
            'campaign_id': self.campaign.id,
            'consumption': 5.0,
        })
        self.assertEqual(invoice.amount_total, 0.0)