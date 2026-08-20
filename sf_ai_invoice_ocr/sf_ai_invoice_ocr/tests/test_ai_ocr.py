from odoo.tests import TransactionCase

class TestAiOcr(TransactionCase):

    def setUp(self):
        super().setUp()
        self.provider = self.env['ai.ocr.provider'].create({
            'name': 'Test Mistral',
            'provider_type': 'mistral',
            'api_key': 'test_key_1234567890123456',
            'model_name': 'pixtral-12b',
        })

    def test_provider_creation(self):
        self.assertEqual(self.provider.provider_type, 'mistral')
        self.assertTrue(self.provider.active)

    def test_ocr_request_creation(self):
        att = self.env['ir.attachment'].create({
            'name': 'test.pdf',
            'datas': 'JVBERi0xLjQK',  # minimal PDF base64
            'mimetype': 'application/pdf',
        })
        req = self.env['ai.ocr.request'].create({
            'provider_id': self.provider.id,
            'attachment_id': att.id,
        })
        self.assertEqual(req.state, 'draft')
        self.assertTrue(req.name.startswith('OCR-'))

    def test_line_creation(self):
        req = self.env['ai.ocr.request'].create({
            'provider_id': self.provider.id,
            'attachment_id': self.env['ir.attachment'].create({
                'name': 'test.pdf', 'datas': 'JVBERi0xLjQK', 'mimetype': 'application/pdf'}).id,
        })
        line = self.env['ai.ocr.line'].create({
            'request_id': req.id,
            'description': 'Test Item',
            'quantity': 2,
            'unit_price': 50.0,
            'tax_rate': 20.0,
        })
        self.assertEqual(line.total, 0.0)  # not auto-computed