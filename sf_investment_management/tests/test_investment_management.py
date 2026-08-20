# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestInvestmentManagement(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Portfolio = self.env['sf.invest.portfolio']
        self.Line = self.env['sf.invest.line']
        self.Valuation = self.env['sf.invest.valuation']
        self.Income = self.env['sf.invest.income']
        self.group_user = self.env.ref(
            'sf_investment_management.group_invest_user')
        self.group_manager = self.env.ref(
            'sf_investment_management.group_invest_manager')
        self.env.user.groups_id += self.group_manager

    def _create_portfolio(self, company=None):
        model = self.Portfolio
        if company:
            model = self.Portfolio.with_company(company)
        return model.create({
            'company_account': 'ACC-001',
            'bank': 'Test Bank',
        })

    def _create_line(self, portfolio, **kwargs):
        vals = {
            'portfolio_id': portfolio.id,
            'security_type': 'stock',
            'security_name': 'Test Stock',
            'quantity': 100.0,
            'cost_price': 50.0,
            'current_price': 60.0,
        }
        vals.update(kwargs)
        return self.Line.create(vals)

    def _create_user(self, name, login, group):
        return self.env['res.users'].create({
            'name': name,
            'login': login,
            'groups_id': [(6, 0, [group.id])],
        })

    def test_create_portfolio_line_valuation_income(self):
        portfolio = self._create_portfolio()
        line = self._create_line(portfolio)
        valuation = self.Valuation.create({
            'line_id': line.id,
            'date': fields.Date.today(),
            'price': 62.0,
        })
        income = self.Income.create({
            'line_id': line.id,
            'income_type': 'dividend',
            'amount': 25.0,
        })
        self.assertTrue(portfolio.name.startswith('PF-'))
        self.assertTrue(line.name.startswith('LIN-'))
        self.assertTrue(valuation.name.startswith('VAL-'))
        self.assertTrue(income.name.startswith('INC-'))
        self.assertEqual(valuation.computed_value, 100.0 * 62.0)

    def test_line_value_and_latent_gain(self):
        line = self._create_line(self._create_portfolio())
        self.assertEqual(line.value, 100.0 * 60.0)
        self.assertEqual(line.latent_gain, (60.0 - 50.0) * 100.0)
        line.current_price = 70.0
        self.assertEqual(line.value, 100.0 * 70.0)
        self.assertEqual(line.latent_gain, (70.0 - 50.0) * 100.0)

    def test_coupon_income_amount_computed(self):
        portfolio = self._create_portfolio()
        line = self._create_line(portfolio, security_type='bond',
                                 coupon_rate=2.5)
        self.assertEqual(line.coupon_expected, 100.0 * 2.5)
        income = self.Income.create({
            'line_id': line.id,
            'income_type': 'coupon',
            'amount': 0.0,
        })
        income.action_received()
        self.assertEqual(income.amount, 100.0 * 2.5)
        self.assertEqual(income.state, 'received')

    def test_income_received_manager_only(self):
        user = self._create_user('Invest User', 'invest_user',
                                 self.group_user)
        portfolio = self._create_portfolio()
        line = self._create_line(portfolio, security_type='bond',
                                 coupon_rate=2.0)
        income = self.Income.create({
            'line_id': line.id,
            'income_type': 'coupon',
            'amount': 0.0,
        })
        with self.assertRaises(UserError):
            income.with_user(user).action_received()
        income.action_received()
        self.assertEqual(income.amount, 100.0 * 2.0)

    def test_maturity_and_cron_alert_dedup(self):
        portfolio = self._create_portfolio()
        today = fields.Date.today()
        near = self._create_line(portfolio, security_type='bond',
                                 maturity_date=today + timedelta(days=2))
        near.state = 'open'
        self.Line._check_invest_alerts()
        self.Line._check_invest_alerts()
        self.assertEqual(len(near.activity_ids), 1)
        past = self._create_line(portfolio, security_type='bond',
                                 maturity_date=today - timedelta(days=1))
        past.state = 'open'
        self.Line._check_invest_alerts()
        self.assertEqual(past.state, 'matured')

    def test_portfolio_close_manager_only(self):
        user = self._create_user('Invest User 2', 'invest_user2',
                                 self.group_user)
        portfolio = self._create_portfolio()
        portfolio.action_open()
        with self.assertRaises(UserError):
            portfolio.with_user(user).action_close()
        portfolio.action_close()
        self.assertEqual(portfolio.state, 'closed')

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Invest Company B'})
        user = self._create_user('Company A User', 'company_a_user',
                                 self.group_user)
        portfolio_b = self._create_portfolio(company=company_b)
        self.assertNotIn(portfolio_b, self.Portfolio.with_user(user).search(
            [('id', '=', portfolio_b.id)]))

    def test_report_records_exist(self):
        performance = self.env['ir.actions.report'].search([
            ('report_name', '=',
             'sf_investment_management.report_performance_template'),
        ])
        self.assertTrue(performance)
        maturities = self.env['ir.actions.report'].search([
            ('model', '=', 'sf.invest.line'),
            ('report_type', '=', 'qweb-pdf'),
        ])
        self.assertTrue(maturities)