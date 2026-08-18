# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestProjectMargin(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Item = self.env['sf.project.budget.item']
        self.Project = self.env['project.project']
        self.project = self.Project.create({
            'name': 'Website Redesign',
        })

    def _add(self, ptype, category, amount):
        return self.Item.create({
            'project_id': self.project.id,
            'type': ptype,
            'category': category,
            'amount': amount,
        })

    def test_01_budget_item_creation(self):
        item = self._add('revenue', 'Fees', 10000.0)
        self.assertEqual(item.type, 'revenue')
        self.assertEqual(item.amount, 10000.0)

    def test_02_margin_computed(self):
        self._add('revenue', 'Fees', 10000.0)
        self._add('cost', 'Team', 6000.0)
        self._add('cost', 'Software', 1000.0)
        self.assertEqual(self.project.sf_budget_revenue, 10000.0)
        self.assertEqual(self.project.sf_budget_cost, 7000.0)
        self.assertEqual(self.project.sf_margin, 3000.0)
        self.assertEqual(self.project.sf_margin_pct, 30.0)

    def test_03_margin_status_ok(self):
        self._add('revenue', 'Fees', 10000.0)
        self._add('cost', 'Team', 2000.0)
        self.assertEqual(self.project.sf_margin_pct, 80.0)
        self.assertEqual(self.project.sf_margin_status, 'ok')

    def test_04_margin_status_warning(self):
        self._add('revenue', 'Fees', 10000.0)
        self._add('cost', 'Team', 8500.0)
        self.assertEqual(self.project.sf_margin_pct, 15.0)
        self.assertEqual(self.project.sf_margin_status, 'warning')

    def test_05_margin_status_critical(self):
        self._add('revenue', 'Fees', 10000.0)
        self._add('cost', 'Team', 9500.0)
        self.assertEqual(self.project.sf_margin_pct, 5.0)
        self.assertEqual(self.project.sf_margin_status, 'critical')

    def test_06_no_revenue(self):
        self._add('cost', 'Team', 1000.0)
        self.assertEqual(self.project.sf_margin_pct, 0.0)