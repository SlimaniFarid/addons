from odoo.tests import TransactionCase

class TestSaleAutoWorkflow(TransactionCase):

    def setUp(self):
        super().setUp()
        self.partner = self.env['res.partner'].create({'name': 'Test Customer'})
        self.product = self.env['product.product'].create({
            'name': 'Test Product', 'type': 'consu', 'list_price': 100.0,
        })
        self.payment_method = self.env.ref('account.account_payment_method_manual_in')

    def test_rule_creation(self):
        rule = self.env['sale.auto.rule'].create({
            'name': 'Test Rule',
            'sequence': 10,
            'action_confirm': True,
            'action_create_invoice': True,
        })
        self.assertTrue(rule.active)
        self.assertEqual(rule.sequence, 10)

    def test_rule_matching(self):
        rule = self.env['sale.auto.rule'].create({
            'name': 'Cash Rule',
            'payment_method_ids': [(6, 0, [self.payment_method.id])],
            'amount_min': 50.0,
            'amount_max': 500.0,
        })
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'payment_method_id': self.payment_method.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'product_uom_qty': 1})],
        })
        self.assertTrue(rule._match_order(order))

        order2 = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'payment_method_id': self.payment_method.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'product_uom_qty': 10})],
        })
        # Amount 1000 > 500 max
        self.assertFalse(rule._match_order(order2))

    def test_rule_application(self):
        rule = self.env['sale.auto.rule'].create({
            'name': 'Auto Confirm',
            'action_confirm': True,
            'action_create_invoice': False,
        })
        order = self.env['sale.order'].create({
            'partner_id': self.partner.id,
            'order_line': [(0, 0, {'product_id': self.product.id, 'product_uom_qty': 1})],
        })
        order.action_confirm()
        self.assertEqual(order.state, 'sale')