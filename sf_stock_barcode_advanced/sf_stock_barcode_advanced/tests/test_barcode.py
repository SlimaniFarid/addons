from odoo.tests import TransactionCase

class TestBarcode(TransactionCase):

    def setUp(self):
        super().setUp()
        self.config = self.env['barcode.config'].create({
            'name': 'Test Config',
        })
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'barcode': '1234567890123',
            'type': 'consu',
        })
        self.picking = self.env['stock.picking'].create({
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'location_id': self.env.ref('stock.stock_location_suppliers').id,
            'location_dest_id': self.env.ref('stock.stock_location_stock').id,
        })

    def test_config_creation(self):
        self.assertTrue(self.config.active)
        self.assertEqual(self.config.pattern_product, r'^\d{12,14}$')

    def test_parse_product_barcode(self):
        parsed = self.config.parse_barcode('1234567890123')
        self.assertEqual(parsed['type'], 'product')
        self.assertEqual(parsed['code'], '1234567890123')

    def test_parse_gs1(self):
        parsed = self.config.parse_barcode('(01)01234567890128(10)LOT123(30)50')
        self.assertEqual(parsed['type'], 'gs1')
        self.assertEqual(parsed['gtin'], '01234567890128')
        self.assertEqual(parsed['lot'], 'LOT123')
        self.assertEqual(parsed['qty'], 50)

    def test_scan_wizard(self):
        wizard = self.env['barcode.scan'].create({
            'config_id': self.config.id,
            'picking_id': self.picking.id,
            'barcode': '1234567890123',
        })
        wizard.action_scan()
        self.assertEqual(wizard.action, 'scan_product')
        self.assertEqual(wizard.product_id, self.product)