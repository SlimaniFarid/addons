from odoo.tests import TransactionCase

class TestDirectPrint(TransactionCase):

    def setUp(self):
        super().setUp()

    def test_printer_creation(self):
        printer = self.env['print.printer'].create({
            'name': 'Test ZPL Printer',
            'printer_type': 'network',
            'host': '192.168.1.100',
            'port': 9100,
        })
        self.assertEqual(printer.printer_type, 'network')
        self.assertTrue(printer.supports_zpl)

    def test_profile_creation(self):
        printer = self.env['print.printer'].create({
            'name': 'Test Printer',
            'printer_type': 'network',
            'host': '192.168.1.100',
        })
        report = self.env.ref('stock.report_delivery_slip', raise_if_not_found=False)
        profile = self.env['print.profile'].create({
            'name': 'Delivery Label',
            'printer_id': printer.id,
            'report_id': report.id if report else False,
            'format': 'zpl',
            'auto_print': True,
            'trigger_model': 'stock.picking',
            'trigger_field': 'state',
            'trigger_value': 'done',
        })
        self.assertEqual(profile.format, 'zpl')
        self.assertTrue(profile.auto_print)

    def test_job_creation(self):
        printer = self.env['print.printer'].create({
            'name': 'Test Printer',
            'printer_type': 'network',
            'host': '192.168.1.100',
        })
        job = self.env['print.job'].create({
            'printer_id': printer.id,
            'model': 'stock.picking',
            'res_id': 1,
            'format': 'zpl',
            'content': 'VGVzdA==',  # base64 'Test'
        })
        self.assertEqual(job.state, 'draft')
        self.assertTrue(job.name.startswith('PRJ-'))