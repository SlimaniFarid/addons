# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


class TestFAI(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Report = self.env['sf.fai.report']
        self.Char = self.env['sf.fai.characteristic']
        self.NC = self.env['sf.fai.nonconformance']
        self.Approval = self.env['sf.fai.approval']
        self.part = self.env['product.product'].create({'name': 'Turbine Blade'})
        self.supplier = self.env['res.partner'].create({'name': 'AeroSupply Co', 'supplier_rank': 1})
        self.customer = self.env['res.partner'].create({'name': 'Boeing', 'customer_rank': 1})

    def test_01_report_creation(self):
        report = self.Report.create({
            'part_id': self.part.id,
            'drawing_number': 'DWG-001',
            'fai_type': 'full',
            'supplier_id': self.supplier.id,
            'customer_id': self.customer.id,
        })
        self.assertEqual(report.state, 'draft')
        self.assertEqual(report.fai_type, 'full')

    def test_02_characteristic_and_accountability(self):
        report = self.Report.create({'part_id': self.part.id, 'fai_type': 'full'})
        self.Char.create({'report_id': report.id, 'characteristic_number': 'C001', 'result': 'pass'})
        self.Char.create({'report_id': report.id, 'characteristic_number': 'C002', 'result': 'fail'})
        self.Char.create({'report_id': report.id, 'characteristic_number': 'C003', 'result': 'not_measured'})
        self.assertEqual(report.total_characteristics, 3)
        self.assertEqual(report.passed_characteristics, 1)
        self.assertEqual(report.failed_characteristics, 1)
        self.assertAlmostEqual(report.accountability_pct, 33.33, places=1)

    def test_03_workflow(self):
        report = self.Report.create({'part_id': self.part.id, 'fai_type': 'full'})
        report.action_start()
        self.assertEqual(report.state, 'in_progress')
        report.action_submit()
        self.assertEqual(report.state, 'submitted')
        # Approval created
        self.assertTrue(report.approval_ids)
        report.action_approve()
        self.assertEqual(report.state, 'approved')

    def test_04_nonconformance_flow(self):
        report = self.Report.create({'part_id': self.part.id, 'fai_type': 'full'})
        char = self.Char.create({'report_id': report.id, 'characteristic_number': 'C001', 'result': 'fail'})
        nc = self.NC.create({
            'report_id': report.id,
            'characteristic_id': char.id,
            'nc_number': 'NC-001',
            'description': 'Diameter out of tolerance',
            'severity': 'major',
        })
        self.assertEqual(nc.state, 'open')
        nc.action_disposition()
        nc.write({'disposition': 'rework', 'disposition_rationale': 'Rework to spec'})
        self.assertEqual(nc.state, 'dispositioned')
        nc.action_close()
        self.assertEqual(nc.state, 'closed')

    def test_05_approval_workflow(self):
        report = self.Report.create({'part_id': self.part.id, 'fai_type': 'full'})
        report.action_submit()
        approval = report.approval_ids[0]
        approval.action_approve()
        self.assertEqual(approval.status, 'approved')
        # All approved -> report approved
        self.assertEqual(report.state, 'approved')

    def test_06_partial_fai(self):
        report = self.Report.create({
            'part_id': self.part.id,
            'fai_type': 'partial',
            'reason_partial': 'Only critical characteristics',
        })
        self.assertEqual(report.fai_type, 'partial')
        self.assertIn('critical', report.reason_partial.lower())