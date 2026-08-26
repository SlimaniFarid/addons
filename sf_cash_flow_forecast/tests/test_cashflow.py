# -*- coding: utf-8 -*-
from datetime import date, timedelta

from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestCashFlowForecast(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.currency = cls.env.ref('base.EUR')
        cls.partner_a = cls.env['res.partner'].create({
            'name': 'Customer A',
        })
        cls.partner_b = cls.env['res.partner'].create({
            'name': 'Vendor B',
        })
        cls.bank_journal = cls.env['account.journal'].create({
            'name': 'Bank Test',
            'type': 'bank',
            'code': 'BKT',
        })
        cls.cash_journal = cls.env['account.journal'].create({
            'name': 'Cash Test',
            'type': 'cash',
            'code': 'CST',
        })

    def _new_forecast(self, horizon=30, alert=0.0):
        today = date.today()
        return self.env['sf.cashflow.forecast'].create({
            'date_from': today,
            'horizon_days': horizon,
            'alert_threshold': alert,
            'bank_journal_ids': [(6, 0, (self.bank_journal + self.cash_journal).ids)],
        })

    def test_01_create_forecast(self):
        forecast = self._new_forecast()
        self.assertTrue(forecast.name)
        self.assertGreater(forecast.date_to, forecast.date_from)
        self.assertEqual(forecast.state, 'draft')
        self.assertIn('CF/', forecast.name)

    def test_02_manual_lines_compute_balances(self):
        forecast = self._new_forecast()
        self.env['sf.cashflow.line'].create([
            {
                'forecast_id': forecast.id,
                'date': forecast.date_from + timedelta(days=5),
                'direction': 'inflow',
                'name': 'Customer payment expected',
                'amount': 1000.0,
                'partner_id': self.partner_a.id,
            },
            {
                'forecast_id': forecast.id,
                'date': forecast.date_from + timedelta(days=10),
                'direction': 'outflow',
                'name': 'Supplier payment planned',
                'amount': 400.0,
                'partner_id': self.partner_b.id,
            },
        ])
        self.assertEqual(forecast.total_inflow, 1000.0)
        self.assertEqual(forecast.total_outflow, 400.0)
        self.assertEqual(forecast.net_cash_flow, 600.0)
        self.assertEqual(forecast.minimum_balance, -400.0)
        self.assertEqual(forecast.minimum_date, forecast.date_from + timedelta(days=10))

    def test_03_generate_lines_no_crash_empty_db(self):
        forecast = self._new_forecast()
        result = forecast.action_generate_lines()
        self.assertTrue(result)
        self.assertTrue(all(
            line.source == 'auto' for line in forecast.line_ids))

    def test_04_alert_generation(self):
        forecast = self._new_forecast(alert=500.0)
        self.env['sf.cashflow.line'].create({
            'forecast_id': forecast.id,
            'date': forecast.date_from + timedelta(days=3),
            'direction': 'outflow',
            'name': 'Big supplier payment',
            'amount': 800.0,
        })
        forecast.action_confirm()
        self.assertEqual(forecast.state, 'confirmed')
        self.assertTrue(forecast.alert_ids)
        self.assertEqual(forecast.alert_ids[0].projected_balance, -800.0)

    def test_05_cancel_and_draft(self):
        forecast = self._new_forecast()
        forecast.action_confirm()
        self.assertEqual(forecast.state, 'confirmed')
        forecast.action_cancel()
        self.assertEqual(forecast.state, 'cancelled')
        forecast.action_draft()
        self.assertEqual(forecast.state, 'draft')

    def test_06_line_negative_amount_constraint(self):
        forecast = self._new_forecast()
        with self.assertRaises(Exception):
            self.env['sf.cashflow.line'].create({
                'forecast_id': forecast.id,
                'date': forecast.date_from,
                'direction': 'inflow',
                'name': 'Bad negative amount',
                'amount': -50.0,
            })