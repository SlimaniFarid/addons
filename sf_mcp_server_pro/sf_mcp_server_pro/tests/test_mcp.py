from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError

class TestMcpServer(TransactionCase):

    def setUp(self):
        super().setUp()
        self.server = self.env['mcp.server'].create({
            'name': 'Test Server',
            'code': 'test1',
            'api_key': 'testapikey12345',
            'allowed_models': 'res.partner,product.product',
        })

    def test_server_creation(self):
        self.assertEqual(self.server.state, 'draft')
        self.assertEqual(self.server.code, 'test1')

    def test_api_key_validation(self):
        with self.assertRaises(ValidationError):
            self.env['mcp.server'].create({
                'name': 'Bad Key',
                'code': 'bad',
                'api_key': 'short',
            })

    def test_allowed_models(self):
        self.assertIn('res.partner', self.server.get_model_list())
        self.assertIn('product.product', self.server.get_model_list())
        self.assertTrue(self.server.is_model_allowed('res.partner'))
        self.assertFalse(self.server.is_model_allowed('sale.order'))

    def test_token_creation(self):
        token = self.env['mcp.token'].create({
            'name': 'Test Token',
            'server_id': self.server.id,
            'token': 'tokenvalue123',
        })
        self.assertEqual(token.server_id, self.server)
        self.assertTrue(token.active)

    def test_log_creation(self):
        log = self.env['mcp.request.log'].create({
            'server_id': self.server.id,
            'tool': 'search_res.partner',
            'model': 'res.partner',
            'status': 'success',
            'response_ms': 50,
        })
        self.assertEqual(log.server_id, self.server)
        self.assertEqual(log.status, 'success')