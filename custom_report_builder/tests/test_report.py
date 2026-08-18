from odoo.tests import TransactionCase

class TestReportBuilder(TransactionCase):

    def setUp(self):
        super().setUp()
        self.model = self.env.ref('account.model_account_move')
        self.template = self.env['report.template'].create({
            'name': 'Test Invoice',
            'model_id': self.model.id,
            'report_name': 'custom_report_builder.test_invoice',
        })

    def test_template_creation(self):
        self.assertEqual(self.template.model_id, self.model)
        self.assertTrue(self.template.active)

    def test_block_creation(self):
        block = self.env['report.block'].create({
            'template_id': self.template.id,
            'block_type': 'field',
            'name': 'Invoice Number',
            'field_name': 'name',
            'field_label': 'Invoice #',
        })
        self.assertEqual(block.block_type, 'field')
        qweb = block.to_qweb()
        self.assertIn('record.name', qweb)

    def test_text_block_qweb(self):
        block = self.env['report.block'].create({
            'template_id': self.template.id,
            'block_type': 'text',
            'text_content': '<p>Hello World</p>',
        })
        qweb = block.to_qweb()
        self.assertIn('Hello World', qweb)

    def test_table_block_qweb(self):
        block = self.env['report.block'].create({
            'template_id': self.template.id,
            'block_type': 'table',
            'table_model': 'invoice_line_ids',
            'table_fields': '[{"name": "product_id", "label": "Product"}, {"name": "price_unit", "label": "Price", "format": "currency"}]',
        })
        qweb = block.to_qweb()
        self.assertIn('invoice_line_ids', qweb)
        self.assertIn('product_id', qweb)

    def test_assignment_creation(self):
        assign = self.env['report.assignment'].create({
            'template_id': self.template.id,
            'report_action_id': self.env.ref('account.account_invoices').id,
        })
        self.assertEqual(assign.template_id, self.template)