from odoo.tests import TransactionCase

class TestWhatsApp(TransactionCase):

    def setUp(self):
        super().setUp()
        self.account = self.env['whatsapp.account'].create({
            'name': 'Test Account',
            'phone_number_id': '123456789',
            'business_account_id': '987654321',
            'access_token': 'test_token_123456789012',
        })

    def test_account_creation(self):
        self.assertEqual(self.account.state, 'draft')
        self.assertEqual(self.account.phone_number_id, '123456789')

    def test_template_creation(self):
        tmpl = self.env['whatsapp.template'].create({
            'account_id': self.account.id,
            'name': 'Order Confirmation',
            'template_name': 'order_confirmation',
            'category': 'utility',
            'language': 'en_US',
            'body_text': 'Hi {{name}}, your order {{order_ref}} is confirmed.',
        })
        self.assertEqual(tmpl.template_name, 'order_confirmation')
        self.assertEqual(tmpl.category, 'utility')

    def test_message_creation(self):
        msg = self.env['whatsapp.message'].create({
            'account_id': self.account.id,
            'to_number': '15551234567',
            'to_name': 'Test User',
            'status': 'draft',
        })
        self.assertEqual(msg.status, 'draft')
        self.assertEqual(msg.direction, 'outbound')