# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestVendorPortal(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Partner = self.env['res.partner']
        self.Purchase = self.env['purchase.order']
        self.partner = self.Partner.create({
            'name': 'Test Vendor',
            'email': 'vendor@example.com',
            'supplier_rank': 1,
        })

    def test_01_vendor_portal_user_creation(self):
        self.assertFalse(self.partner.portal_user_id)
        self.partner.action_create_portal_user()
        self.assertTrue(self.partner.portal_user_id)
        self.assertTrue(self.partner.is_vendor_portal_user)
        self.assertTrue(self.partner.portal_welcome_sent)

    def test_02_rfq_vendor_accept(self):
        order = self.Purchase.create({
            'partner_id': self.partner.id,
        })
        order.action_vendor_accept()
        self.assertEqual(order.vendor_response, 'accepted')
        self.assertTrue(order.vendor_response_date)

    def test_03_rfq_vendor_decline(self):
        order = self.Purchase.create({
            'partner_id': self.partner.id,
        })
        order.action_vendor_decline('Too expensive for this budget.')
        self.assertEqual(order.vendor_response, 'declined')
        self.assertEqual(
            order.vendor_comment, 'Too expensive for this budget.')

    def test_04_rfq_vendor_counter(self):
        order = self.Purchase.create({
            'partner_id': self.partner.id,
        })
        order.action_vendor_counter(1250.50)
        self.assertEqual(order.vendor_response, 'counter')
        self.assertEqual(order.counter_total, 1250.50)

    def test_05_portal_access_key_generated(self):
        order = self.Purchase.create({
            'partner_id': self.partner.id,
        })
        self.assertTrue(order.portal_access_key)

    def test_06_vendor_counts(self):
        self.Purchase.create({'partner_id': self.partner.id})
        self.assertEqual(self.partner.total_quotation_count, 1)
        self.assertEqual(self.partner.total_confirmed_orders, 0)

    def test_07_settings_default(self):
        settings = self.env['sf.vendor.portal.settings']._get_settings()
        self.assertTrue(settings)
        self.assertTrue(settings.welcome_message)

    def test_08_idempotent_portal_user(self):
        self.partner.action_create_portal_user()
        first_user = self.partner.portal_user_id
        self.partner.action_create_portal_user()
        self.assertEqual(self.partner.portal_user_id, first_user)