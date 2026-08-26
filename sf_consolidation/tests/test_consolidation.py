# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestConsolidation(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Group = self.env['sf.consolidation.group']
        self.Period = self.env['sf.consolidation.period']
        self.Line = self.env['sf.consolidation.line']
        self.company1 = self.env.company
        self.company2 = self.env['res.company'].create({
            'name': 'Subsidiary Co',
        })
        self.group = self.Group.create({
            'name': 'HoldCo Group',
            'code': 'HCG',
            'company_ids': [(6, 0, [self.company1.id, self.company2.id])],
        })
        self.account = self.env['account.account'].search(
            [('company_ids', 'in', self.company1.ids)], limit=1)

    def test_01_group_creation(self):
        self.assertEqual(self.group.code, 'HCG')
        self.assertEqual(len(self.group.company_ids), 2)

    def test_02_group_code_unique(self):
        with self.assertRaises(Exception):
            self.Group.create({
                'name': 'Other', 'code': 'HCG',
                'company_ids': [(6, 0, [self.company1.id])]})

    def test_03_period_creation(self):
        period = self.group.action_create_period(
            '2026-01-01', '2026-01-31')
        self.assertEqual(period.group_id, self.group)
        self.assertEqual(period.state, 'draft')

    def test_04_line_and_total(self):
        period = self.group.action_create_period('2026-01-01', '2026-01-31')
        self.Line.create({
            'period_id': period.id,
            'company_id': self.company1.id,
            'account_id': self.account.id,
            'amount': 1000.0,
        })
        self.Line.create({
            'period_id': period.id,
            'company_id': self.company2.id,
            'account_id': self.account.id,
            'amount': 500.0,
        })
        self.assertEqual(period.total_balance, 1500.0)

    def test_05_done_state(self):
        period = self.group.action_create_period('2026-01-01', '2026-01-31')
        period.action_done()
        self.assertEqual(period.state, 'done')

    def test_06_generate_from_moves_no_lines(self):
        period = self.group.action_create_period('2020-01-01', '2020-12-31')
        period.action_generate_from_moves()
        # no posted moves -> no lines
        self.assertEqual(len(period.line_ids), 0)