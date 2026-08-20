# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestPriceMatrix(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Category = self.env['sf.price.matrix.category']
        self.Tier = self.env['sf.price.matrix.tier']
        self.Rule = self.env['sf.price.matrix.rule']
        self.Product = self.env['product.product']
        self.category = self.Category.create({
            'name': 'Wholesale',
            'code': 'WS',
            'default_discount': 5.0,
        })
        self.tier_50 = self.Tier.create({
            'name': 'Vol 50', 'min_qty': 50, 'discount': 10.0,
        })
        self.tier_200 = self.Tier.create({
            'name': 'Vol 200', 'min_qty': 200, 'discount': 15.0,
        })
        self.product = self.Product.create({
            'name': 'Widget Pro', 'list_price': 100.0,
        })

    def test_01_category_creation(self):
        self.assertEqual(self.category.code, 'WS')
        self.assertEqual(self.category.default_discount, 5.0)

    def test_02_category_code_unique(self):
        with self.assertRaises(Exception):
            self.Category.create({'name': 'Wholesale 2', 'code': 'WS'})

    def test_03_tier_creation(self):
        self.assertEqual(self.tier_50.discount, 10.0)
        self.assertEqual(self.tier_200.min_qty, 200)

    def test_04_rule_creation(self):
        rule = self.Rule.create({
            'category_id': self.category.id,
            'product_id': self.product.id,
            'tier_ids': [(6, 0, [self.tier_50.id, self.tier_200.id])],
            'max_discount': 20.0,
        })
        self.assertEqual(len(rule.tier_ids), 2)

    def test_05_rule_unique_per_product(self):
        self.Rule.create({
            'category_id': self.category.id, 'product_id': self.product.id,
        })
        with self.assertRaises(Exception):
            self.Rule.create({
                'category_id': self.category.id,
                'product_id': self.product.id,
            })

    def test_06_default_discount_when_no_rule(self):
        disc = self.Rule.compute_discount(self.category, self.product, 10)
        self.assertEqual(disc, 5.0)

    def test_07_tier_discount_applied(self):
        rule = self.Rule.create({
            'category_id': self.category.id,
            'product_id': self.product.id,
            'tier_ids': [(6, 0, [self.tier_50.id, self.tier_200.id])],
            'max_discount': 20.0,
        })
        # qty 10 -> default 5
        self.assertEqual(self.Rule.compute_discount(
            self.category, self.product, 10), 5.0)
        # qty 60 -> tier 50 -> 10
        self.assertEqual(self.Rule.compute_discount(
            self.category, self.product, 60), 10.0)
        # qty 300 -> tier 200 -> 15
        self.assertEqual(self.Rule.compute_discount(
            self.category, self.product, 300), 15.0)

    def test_08_max_discount_cap(self):
        self.Rule.create({
            'category_id': self.category.id,
            'product_id': self.product.id,
            'tier_ids': [(6, 0, [self.tier_200.id])],
            'max_discount': 12.0,
        })
        # tier 200 gives 15 but capped at 12
        self.assertEqual(self.Rule.compute_discount(
            self.category, self.product, 300), 12.0)