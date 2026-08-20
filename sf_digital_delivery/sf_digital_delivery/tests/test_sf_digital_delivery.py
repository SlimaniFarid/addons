# -*- coding: utf-8 -*-
import uuid
from datetime import datetime, timedelta

from odoo import fields as odoo_fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfDigitalDelivery(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })
        self.product = self.env['product.template'].create({
            'name': 'Software License %s' % uuid.uuid4().hex[:4],
            'type': 'service',
        })
        self.digital_product = self.env['sf.digital.product'].create({
            'product_id': self.product.id,
            'delivery_type': 'license_key',
            'max_activations': 1,
            'validity_days': 30,
        })
        self.pricelist = self.env['product.pricelist'].create({
            'name': 'Test Pricelist %s' % uuid.uuid4().hex[:4],
            'currency_id': self.env.company.currency_id.id,
        })

    def _create_sale_order(self, product=None, qty=2):
        product = product or self.product
        order = self.env['sale.order'].create({
            'partner_id': self.customer.id,
            'pricelist_id': self.pricelist.id,
            'order_line': [(0, 0, {
                'product_id': product.product_variant_id.id,
                'product_uom_qty': qty,
            })],
        })
        order.action_confirm()
        return order

    def _delivery_of(self, order):
        return self.env['sf.digital.delivery'].search([('order_id', '=', order.id)], limit=1)

    def test_sequences(self):
        product = self.env['sf.digital.product'].create({
            'product_id': self.product.id,
            'delivery_type': 'download',
        })
        self.assertTrue(product.name.startswith('DIG-'))
        key = self.env['sf.digital.key'].create({
            'product_id': self.digital_product.id,
            'key': 'ABCD-1234-EFGH',
        })
        self.assertTrue(key.name.startswith('KEY-'))
        order = self.env['sale.order'].create({'partner_id': self.customer.id})
        delivery = self.env['sf.digital.delivery'].create({'order_id': order.id})
        self.assertTrue(delivery.name.startswith('DEL-'))
        line = self.env['sf.digital.delivery.line'].create({
            'delivery_id': delivery.id,
            'product_id': self.product.id,
            'digital_product_id': self.digital_product.id,
            'quantity': 2,
        })
        self.assertTrue(line.name.startswith('DDL-'))

    def test_order_confirm_creates_delivery(self):
        order = self._create_sale_order(qty=3)
        delivery = self._delivery_of(order)
        self.assertTrue(delivery)
        self.assertEqual(delivery.state, 'draft')
        self.assertEqual(delivery.partner_id, self.customer)
        self.assertEqual(delivery.line_ids.quantity, 3)
        self.assertEqual(delivery.line_ids.digital_product_id, self.digital_product)

    def test_order_without_digital_product_no_delivery(self):
        other = self.env['product.template'].create({
            'name': 'Physical Product %s' % uuid.uuid4().hex[:4],
            'type': 'consu',
        })
        order = self._create_sale_order(product=other, qty=1)
        self.assertFalse(self._delivery_of(order))

    def test_generate_keys_count_and_uniqueness(self):
        order = self._create_sale_order(qty=3)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        self.assertEqual(delivery.state, 'generated')
        keys = delivery.line_ids.key_ids
        self.assertEqual(len(keys), 3)
        self.assertEqual(len(set(keys.mapped('key'))), 3)
        for key in keys:
            self.assertEqual(key.state, 'generated')
            self.assertEqual(len(key.key.split('-')), 3)
            self.assertTrue(all(len(part) == 4 for part in key.key.split('-')))

    def test_generate_download_link(self):
        download_product = self.env['product.template'].create({
            'name': 'Ebook %s' % uuid.uuid4().hex[:4],
            'type': 'service',
        })
        digital_download = self.env['sf.digital.product'].create({
            'product_id': download_product.id,
            'delivery_type': 'download',
            'validity_days': 15,
        })
        order = self._create_sale_order(product=download_product, qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        self.assertTrue(delivery.line_ids.download_url)
        self.assertEqual(delivery.state, 'generated')

    def test_workflow_deliver(self):
        order = self._create_sale_order(qty=2)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        self.assertEqual(delivery.state, 'delivered')
        self.assertTrue(delivery.delivery_date)
        self.assertTrue(all(key.state == 'delivered' for key in delivery.line_ids.key_ids))

    def test_deliver_without_keys_failed(self):
        order = self._create_sale_order(qty=2)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.line_ids.key_ids.unlink()
        with self.assertRaises(UserError):
            delivery.action_deliver()
        self.assertEqual(delivery.state, 'failed')

    def test_deliver_requires_generated(self):
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        with self.assertRaises(UserError):
            delivery.action_deliver()

    def test_activation_limits(self):
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        key = delivery.line_ids.key_ids
        key.action_activate()
        self.assertEqual(key.state, 'activated')
        self.assertEqual(key.activation_count, 1)
        with self.assertRaises(UserError):
            key.action_activate()

    def test_activation_requires_delivered(self):
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        key = delivery.line_ids.key_ids
        self.assertEqual(key.state, 'generated')
        with self.assertRaises(UserError):
            key.action_activate()

    def test_multi_activation_up_to_max(self):
        self.digital_product.max_activations = 3
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        key = delivery.line_ids.key_ids
        key.action_activate()
        key.action_activate()
        self.assertEqual(key.activation_count, 2)
        key.action_activate()
        self.assertEqual(key.activation_count, 3)
        with self.assertRaises(UserError):
            key.action_activate()

    def test_revoke(self):
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        key = delivery.line_ids.key_ids
        key.action_revoke()
        self.assertEqual(key.state, 'revoked')

    def test_cancel_draft_delivery(self):
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        delivery.action_cancel()
        self.assertEqual(delivery.state, 'cancelled')

    def test_cancel_delivered_blocked(self):
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        with self.assertRaises(UserError):
            delivery.action_cancel()
        with self.assertRaises(UserError):
            delivery.write({'state': 'draft'})

    def test_cron_expires_keys(self):
        self.env['ir.config_parameter'].set_param(
            'sf_digital_delivery.default_activation_days', '1')
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        key = delivery.line_ids.key_ids
        key.delivered_date = odoo_fields.Datetime.now() - timedelta(days=2)
        delivery._cron_daily_checks()
        self.assertEqual(key.state, 'expired')

    def test_cron_expires_download_links(self):
        download_product = self.env['product.template'].create({
            'name': 'Ebook %s' % uuid.uuid4().hex[:4],
            'type': 'service',
        })
        digital_download = self.env['sf.digital.product'].create({
            'product_id': download_product.id,
            'delivery_type': 'download',
            'validity_days': 1,
        })
        order = self._create_sale_order(product=download_product, qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        delivery.delivery_date = odoo_fields.Datetime.now() - timedelta(days=2)
        delivery._cron_daily_checks()
        self.assertTrue(delivery.line_ids.download_expired)
        self.assertTrue(delivery.activity_ids)

    def test_active_key_not_expired(self):
        self.env['ir.config_parameter'].set_param(
            'sf_digital_delivery.default_activation_days', '1')
        order = self._create_sale_order(qty=1)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        key = delivery.line_ids.key_ids
        key.action_activate()
        delivery._cron_daily_checks()
        self.assertEqual(key.state, 'activated')

    def test_permissions(self):
        user = self.env['res.users'].create({
            'name': 'Digital User %s' % uuid.uuid4().hex[:4],
            'login': 'dig_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_digital_delivery.group_sf_digital_delivery_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        order = self._create_sale_order(qty=2)
        delivery = self._delivery_of(order)
        with self.assertRaises(UserError):
            delivery.with_user(user).action_generate_keys()
        delivery.action_generate_keys()
        with self.assertRaises(UserError):
            delivery.with_user(user).action_deliver()
        other = self._create_sale_order(qty=1)
        draft = self._delivery_of(other)
        draft.with_user(user).action_cancel()
        self.assertEqual(draft.state, 'cancelled')

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Digital Co 2'})
        digital2 = self.env['sf.digital.product'].with_company(company2).create({
            'product_id': self.product.id,
            'delivery_type': 'license_key',
            'company_id': company2.id,
        })
        order2 = self.env['sale.order'].with_company(company2).create({
            'partner_id': self.customer.id,
            'pricelist_id': self.pricelist.id,
            'company_id': company2.id,
            'order_line': [(0, 0, {
                'product_id': self.product.product_variant_id.id,
                'product_uom_qty': 1,
            })],
        })
        order2.action_confirm()
        delivery2 = self._delivery_of(order2)
        self.assertEqual(delivery2.company_id, company2)
        user = self.env['res.users'].create({
            'name': 'Digital User %s' % uuid.uuid4().hex[:4],
            'login': 'dig_user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref(
                'sf_digital_delivery.group_sf_digital_delivery_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
            'company_id': self.env.company.id,
        })
        visible = self.env['sf.digital.delivery'].with_user(user).search(
            [('id', '=', delivery2.id)])
        self.assertFalse(visible)

    def test_report_generation(self):
        order = self._create_sale_order(qty=2)
        delivery = self._delivery_of(order)
        delivery.action_generate_keys()
        delivery.action_deliver()
        action = self.env.ref(
            'sf_digital_delivery.action_report_digital_delivery').report_action(delivery)
        self.assertTrue(action)
        action = self.env.ref(
            'sf_digital_delivery.action_report_license_key').report_action(
            delivery.line_ids.key_ids)
        self.assertTrue(action)