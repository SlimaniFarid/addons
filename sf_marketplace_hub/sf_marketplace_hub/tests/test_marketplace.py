# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestMarketplace(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Marketplace = self.env['sf.marketplace']
        self.Vendor = self.env['sf.marketplace.vendor']
        self.Listing = self.env['sf.marketplace.listing']
        self.Payout = self.env['sf.marketplace.payout']
        self.Partner = self.env['res.partner']
        self.Product = self.env['product.product']
        self.partner = self.Partner.create({
            'name': 'Market Vendor',
            'supplier_rank': 1,
        })
        self.product = self.Product.create({
            'name': 'Test Product',
            'list_price': 100.0,
        })
        self.marketplace = self.Marketplace.create({
            'name': 'Web Store',
            'code': 'WEB',
        })

    def test_01_marketplace_creation(self):
        self.assertEqual(self.marketplace.code, 'WEB')
        self.assertTrue(self.marketplace.currency_id)

    def test_02_code_unique(self):
        with self.assertRaises(Exception):
            self.Marketplace.create({
                'name': 'Duplicate',
                'code': 'WEB',
            })

    def test_03_vendor_commission_compute(self):
        vendor = self.Vendor.create({
            'partner_id': self.partner.id,
            'marketplace_id': self.marketplace.id,
            'commission_rate': 10.0,
        })
        self.Listing.create({
            'product_id': self.product.id,
            'vendor_id': vendor.id,
            'marketplace_id': self.marketplace.id,
            'sold_qty': 5.0,
        })
        self.assertEqual(vendor.sales_total, 500.0)
        self.assertEqual(vendor.commission_total, 50.0)

    def test_04_listing_states(self):
        vendor = self.Vendor.create({
            'partner_id': self.partner.id,
            'marketplace_id': self.marketplace.id,
        })
        listing = self.Listing.create({
            'product_id': self.product.id,
            'vendor_id': vendor.id,
            'marketplace_id': self.marketplace.id,
        })
        self.assertEqual(listing.state, 'draft')
        listing.action_list()
        self.assertEqual(listing.state, 'listed')
        listing.action_pause()
        self.assertEqual(listing.state, 'paused')
        listing.action_close()
        self.assertEqual(listing.state, 'closed')

    def test_05_payout_sequence(self):
        vendor = self.Vendor.create({
            'partner_id': self.partner.id,
            'marketplace_id': self.marketplace.id,
        })
        payout = self.Payout.create({
            'vendor_id': vendor.id,
            'marketplace_id': self.marketplace.id,
        })
        self.assertTrue(payout.name)
        self.assertNotEqual(payout.name, '/')

    def test_06_payout_workflow(self):
        vendor = self.Vendor.create({
            'partner_id': self.partner.id,
            'marketplace_id': self.marketplace.id,
        })
        payout = self.Payout.create({
            'vendor_id': vendor.id,
            'marketplace_id': self.marketplace.id,
        })
        payout.action_approve()
        self.assertEqual(payout.state, 'approved')
        payout.action_pay()
        self.assertEqual(payout.state, 'paid')

    def test_07_marketplace_totals(self):
        vendor = self.Vendor.create({
            'partner_id': self.partner.id,
            'marketplace_id': self.marketplace.id,
            'commission_rate': 20.0,
        })
        self.Listing.create({
            'product_id': self.product.id,
            'vendor_id': vendor.id,
            'marketplace_id': self.marketplace.id,
            'sold_qty': 10.0,
        })
        self.assertEqual(self.marketplace.gmv_total, 1000.0)
        self.assertEqual(self.marketplace.commission_total, 200.0)

    def test_08_vendor_unique_per_marketplace(self):
        self.Vendor.create({
            'partner_id': self.partner.id,
            'marketplace_id': self.marketplace.id,
        })
        with self.assertRaises(Exception):
            self.Vendor.create({
                'partner_id': self.partner.id,
                'marketplace_id': self.marketplace.id,
            })