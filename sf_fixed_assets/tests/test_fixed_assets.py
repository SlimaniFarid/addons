# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestFixedAssets(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Category = self.env['sf.fixed.asset.category']
        self.Asset = self.env['sf.fixed.asset']
        self.category = self.Category.create({
            'name': 'Machinery',
            'code': 'MACH',
            'useful_life_months': 24,
            'depreciation_method': 'straight_line',
        })

    def test_01_category_creation(self):
        self.assertEqual(self.category.useful_life_months, 24)
        self.assertEqual(self.category.depreciation_method, 'straight_line')

    def test_02_category_name_unique(self):
        with self.assertRaises(Exception):
            self.Category.create({'name': 'Machinery'})

    def test_03_asset_category_fields(self):
        asset = self.Asset.create({
            'name': 'CNC Machine',
            'code': 'FA-001',
            'category_id': self.category.id,
            'purchase_date': '2026-01-15',
            'purchase_value': 12000.0,
        })
        self.assertEqual(asset.useful_life_months, 24)
        self.assertEqual(asset.depreciation_method, 'straight_line')
        self.assertEqual(asset.monthly_depreciation, 500.0)

    def test_04_depreciation_plan(self):
        asset = self.Asset.create({
            'name': 'CNC Machine',
            'code': 'FA-002',
            'category_id': self.category.id,
            'purchase_date': '2026-01-15',
            'purchase_value': 12000.0,
        })
        asset.action_generate_depreciation()
        self.assertEqual(len(asset.depreciation_ids), 24)
        total = sum(asset.depreciation_ids.mapped('amount'))
        self.assertAlmostEqual(total, 12000.0, places=1)

    def test_05_book_value(self):
        asset = self.Asset.create({
            'name': 'CNC Machine',
            'code': 'FA-003',
            'category_id': self.category.id,
            'purchase_date': '2026-01-15',
            'purchase_value': 12000.0,
        })
        asset.action_generate_depreciation()
        self.assertEqual(asset.book_value, 12000.0)
        asset.depreciation_ids[0].write({'amount': 500.0})
        self.assertEqual(asset.accumulated_depreciation, 500.0)
        self.assertEqual(asset.book_value, 11500.0)

    def test_06_residual_value(self):
        asset = self.Asset.create({
            'name': 'Van',
            'code': 'FA-004',
            'category_id': self.category.id,
            'purchase_date': '2026-01-15',
            'purchase_value': 10000.0,
            'residual_value': 1000.0,
        })
        asset.action_generate_depreciation()
        # 9000 depreciable over 24 months = 375/month
        self.assertEqual(asset.monthly_depreciation, 375.0)
        total = sum(asset.depreciation_ids.mapped('amount'))
        self.assertAlmostEqual(total, 9000.0, places=1)

    def test_07_asset_workflow(self):
        asset = self.Asset.create({
            'name': 'Server',
            'code': 'FA-005',
            'category_id': self.category.id,
            'purchase_date': '2026-01-15',
            'purchase_value': 3000.0,
        })
        self.assertEqual(asset.state, 'draft')
        asset.action_in_use()
        self.assertEqual(asset.state, 'in_use')
        asset.action_dispose()
        self.assertEqual(asset.state, 'disposed')

    def test_08_negative_depreciation_blocked(self):
        asset = self.Asset.create({
            'name': 'Printer',
            'code': 'FA-006',
            'category_id': self.category.id,
            'purchase_date': '2026-01-15',
            'purchase_value': 500.0,
        })
        asset.action_generate_depreciation()
        with self.assertRaises(Exception):
            asset.depreciation_ids[0].write({'amount': -10.0})