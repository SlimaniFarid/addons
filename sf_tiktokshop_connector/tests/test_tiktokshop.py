from odoo.tests import TransactionCase

class TestTikTokShop(TransactionCase):

    def setUp(self):
        super().setUp()
        self.store = self.env['tiktokshop.store'].create({
            'name': 'Test Shop',
            'shop_id': 'test_shop_123',
            'shop_cipher': 'cipher_123',
            'region': 'US',
            'app_key': 'test_app_key',
            'app_secret': 'test_app_secret_1234567890123456',
            'access_token': 'test_access_token_1234567890123456',
        })

    def test_store_creation(self):
        self.assertEqual(self.store.state, 'draft')
        self.assertEqual(self.store.region, 'US')

    def test_product_creation(self):
        prod = self.env['tiktokshop.product'].create({
            'store_id': self.store.id,
            'tiktok_product_id': 'tt_prod_123',
            'name': 'Test Product',
            'status': 'active',
        })
        self.assertEqual(prod.store_id, self.store)
        self.assertEqual(prod.tiktok_product_id, 'tt_prod_123')

    def test_order_creation(self):
        order = self.env['tiktokshop.order'].create({
            'store_id': self.store.id,
            'tiktok_order_id': 'tt_order_123',
            'order_status': 'pending',
            'total_amount': 99.99,
            'currency': 'USD',
        })
        self.assertEqual(order.order_status, 'pending')
        self.assertEqual(order.total_amount, 99.99)

    def test_sync_log_creation(self):
        log = self.env['tiktokshop.sync.log'].create({
            'store_id': self.store.id,
            'operation': 'products',
            'direction': 'pull',
            'status': 'running',
        })
        self.assertEqual(log.status, 'running')
        self.assertEqual(log.records_processed, 0)