# -*- coding: utf-8 -*-
import re

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestEsgReporting(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Indicator = self.env['sf.esg.indicator']
        self.Period = self.env['sf.esg.period']
        self.Value = self.env['sf.esg.value']
        self.group_user = self.env.ref('sf_esg_reporting.group_esg_user')
        self.group_manager = self.env.ref(
            'sf_esg_reporting.group_esg_manager')

    def _create_indicator(self, code='KPI-ENERGY'):
        return self.Indicator.create({
            'code': code,
            'category': 'environment',
            'unit': 'kwh',
            'direction': 'less_is_better',
            'frequency': 'monthly',
        })

    def _create_period(self, date_from, date_to):
        return self.Period.create({
            'date_from': date_from,
            'date_to': date_to,
        })

    def test_create_indicator_with_sequence(self):
        indicator = self.Indicator.create({
            'code': 'KPI-WATER',
            'category': 'environment',
            'unit': 'm3',
            'direction': 'less_is_better',
            'frequency': 'monthly',
        })
        self.assertTrue(indicator.name.startswith('KPI-'))

    def test_create_period_with_sequence(self):
        period = self._create_period('2026-01-01', '2026-01-31')
        self.assertTrue(re.match(r'^ESG-\d{4}-P\d+$', period.name))

    def test_value_uniqueness(self):
        indicator = self._create_indicator()
        period = self._create_period('2026-01-01', '2026-01-31')
        self.Value.create({
            'period_id': period.id,
            'indicator_id': indicator.id,
            'value': 100.0,
        })
        with self.assertRaises(Exception):
            self.Value.create({
                'period_id': period.id,
                'indicator_id': indicator.id,
                'value': 200.0,
            })

    def test_variation_and_target_achievement(self):
        indicator = self._create_indicator()
        period1 = self._create_period('2026-01-01', '2026-01-31')
        value1 = self.Value.create({
            'period_id': period1.id,
            'indicator_id': indicator.id,
            'value': 80.0,
            'target': 100.0,
        })
        period1.action_submit()
        period1.action_approve()
        self.assertEqual(value1.achieved, 0.8)
        period2 = self._create_period('2026-02-01', '2026-02-28')
        value2 = self.Value.create({
            'period_id': period2.id,
            'indicator_id': indicator.id,
            'value': 100.0,
            'target': 100.0,
        })
        period2.action_submit()
        period2.action_approve()
        self.assertEqual(value2.achieved, 1.0)
        self.assertEqual(value2.variation, 25.0)

    def test_workflow_submit_approve_manager_only(self):
        period = self._create_period('2026-01-01', '2026-01-31')
        period.action_submit()
        self.assertEqual(period.state, 'submitted')
        self.assertTrue(period.submitted_date)
        user = self.env['res.users'].create({
            'name': 'ESG Collector',
            'login': 'esg_collector',
            'groups_id': [(4, self.group_user.id)],
        })
        with self.assertRaises(UserError):
            period.with_user(user).action_approve()
        period.action_approve()
        self.assertEqual(period.state, 'approved')
        self.assertTrue(period.approved_date)
        self.assertEqual(period.approved_by.id, self.env.user.id)
        period.action_close()
        self.assertEqual(period.state, 'closed')

    def test_approve_submitted_only(self):
        period = self._create_period('2026-01-01', '2026-01-31')
        with self.assertRaises(UserError):
            period.action_approve()

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'ESG Company B'})
        user = self.env['res.users'].create({
            'name': 'ESG Company A User',
            'login': 'esg_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        other = self.Period.with_company(company_b).create({
            'date_from': '2026-01-01',
            'date_to': '2026-01-31',
        })
        self.assertNotIn(other, self.Period.with_user(user).search(
            [('id', '=', other.id)]))

    def test_report_pdf_name_exists(self):
        report = self.env.ref('sf_esg_reporting.report_esg')
        self.assertEqual(report.report_type, 'qweb-pdf')
        self.assertEqual(report.model, 'sf.esg.period')