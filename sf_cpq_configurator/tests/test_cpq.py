# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestCpq(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Attribute = self.env['sf.cpq.attribute']
        self.Option = self.env['sf.cpq.option']
        self.Configurator = self.env['sf.cpq.configurator']
        self.Configuration = self.env['sf.cpq.configuration']
        self.Product = self.env['product.product']
        self.attribute = self.Attribute.create({
            'name': 'Material',
            'code': 'MAT',
        })
        self.opt_steel = self.Option.create({
            'attribute_id': self.attribute.id,
            'name': 'Steel',
            'code': 'STEEL',
            'price_adjust': 50.0,
        })
        self.opt_alu = self.Option.create({
            'attribute_id': self.attribute.id,
            'name': 'Aluminium',
            'code': 'ALU',
            'price_adjust': 120.0,
        })
        self.product = self.Product.create({
            'name': 'Custom Frame',
            'type': 'consu',
            'list_price': 1000.0,
        })

    def test_01_attribute_creation(self):
        self.assertEqual(self.attribute.name, 'Material')
        self.assertEqual(self.attribute.code, 'MAT')
        self.assertEqual(len(self.attribute.option_ids), 2)

    def test_02_attribute_name_unique(self):
        with self.assertRaises(Exception):
            self.Attribute.create({'name': 'Material', 'code': 'MAT2'})

    def test_03_option_unique_per_attribute(self):
        with self.assertRaises(Exception):
            self.Option.create({
                'attribute_id': self.attribute.id,
                'name': 'Steel X',
                'code': 'STEEL',
            })

    def test_04_configurator_creation(self):
        cfg = self.Configurator.create({
            'product_id': self.product.id,
            'attribute_ids': [(6, 0, [self.attribute.id])],
        })
        self.assertEqual(cfg.product_id, self.product)
        self.assertEqual(cfg.attribute_ids, self.attribute)

    def test_05_configurator_unique_per_product(self):
        self.Configurator.create({'product_id': self.product.id})
        with self.assertRaises(Exception):
            self.Configurator.create({'product_id': self.product.id})

    def test_06_price_computation(self):
        cfg = self.Configurator.create({'product_id': self.product.id})
        config = self.Configuration.create({
            'configurator_id': cfg.id,
            'option_ids': [(6, 0, [self.opt_steel.id, self.opt_alu.id])],
            'quantity': 2.0,
        })
        self.assertEqual(config.base_price, 1000.0)
        self.assertEqual(config.adjustments, 170.0)
        self.assertEqual(config.total_price, 2340.0)

    def test_07_configuration_reference(self):
        cfg = self.Configurator.create({'product_id': self.product.id})
        config = self.Configuration.create({'configurator_id': cfg.id})
        self.assertTrue(config.name.startswith('CPQ/'))

    def test_08_quote_generation(self):
        partner = self.env['res.partner'].create({'name': 'ACME Corp'})
        cfg = self.Configurator.create({'product_id': self.product.id})
        config = self.Configuration.create({
            'configurator_id': cfg.id,
            'partner_id': partner.id,
            'quantity': 1.0,
        })
        action = config.action_quote()
        self.assertEqual(action['res_model'], 'sale.order')
        self.assertEqual(config.state, 'quoted')
        order = self.env['sale.order'].browse(action['res_id'])
        self.assertEqual(len(order.order_line), 1)
        self.assertEqual(order.order_line.price_unit, 1000.0)