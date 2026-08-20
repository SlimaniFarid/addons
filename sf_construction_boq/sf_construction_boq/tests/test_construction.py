from odoo.exceptions import UserError
from odoo.tests import TransactionCase


class TestConstructionBoq(TransactionCase):

    def setUp(self):
        super().setUp()
        self.project = self.env['project.project'].create({'name': 'Test Building'})
        self.client = self.env['res.partner'].create({'name': 'Test Client'})
        self.contractor = self.env['res.partner'].create({'name': 'Test Contractor'})

    def test_boq_create_and_compute(self):
        boq = self.env['construction.boq'].create({
            'project_id': self.project.id,
            'partner_id': self.client.id,
        })
        self.assertTrue(boq.name)
        self.assertEqual(boq.state, 'draft')
        self.assertEqual(boq.amount_total, 0.0)
        self.env['construction.boq.line'].create([
            {'boq_id': boq.id, 'description': 'Earthwork', 'quantity': 100.0, 'unit_price': 10.0},
            {'boq_id': boq.id, 'description': 'Concrete', 'quantity': 50.0, 'unit_price': 40.0},
        ])
        self.assertEqual(boq.amount_total, 100.0 * 10.0 + 50.0 * 40.0)

    def test_boq_workflow(self):
        boq = self.env['construction.boq'].create({
            'project_id': self.project.id,
            'partner_id': self.client.id,
        })
        with self.assertRaises(UserError):
            boq.action_confirm()
        self.env['construction.boq.line'].create({
            'boq_id': boq.id, 'description': 'Roofing', 'quantity': 10.0, 'unit_price': 5.0,
        })
        boq.action_confirm()
        self.assertEqual(boq.state, 'confirmed')
        boq.action_start()
        self.assertEqual(boq.state, 'in_progress')
        boq.action_done()
        self.assertEqual(boq.state, 'done')
        with self.assertRaises(UserError):
            boq.action_cancel()

    def test_subcontract_workflow(self):
        subcontract = self.env['construction.subcontract'].create({
            'project_id': self.project.id,
            'contractor_id': self.contractor.id,
            'contract_amount': 5000.0,
            'retention_rate': 10.0,
        })
        self.assertTrue(subcontract.name)
        self.assertEqual(subcontract.state, 'draft')
        subcontract.action_confirm()
        self.assertEqual(subcontract.state, 'confirmed')
        subcontract.action_start()
        self.assertEqual(subcontract.state, 'in_progress')
        subcontract.action_close()
        self.assertEqual(subcontract.state, 'closed')
        with self.assertRaises(UserError):
            subcontract.action_cancel()

    def test_certificate_computation(self):
        subcontract = self.env['construction.subcontract'].create({
            'project_id': self.project.id,
            'contractor_id': self.contractor.id,
            'contract_amount': 5000.0,
            'retention_rate': 10.0,
        })
        subcontract.action_confirm()
        certificate = self.env['construction.payment.certificate'].create({
            'subcontract_id': subcontract.id,
            'project_id': self.project.id,
            'contractor_id': self.contractor.id,
            'period_start': '2026-01-01',
            'period_end': '2026-01-31',
            'retention_rate': 10.0,
        })
        self.env['construction.payment.certificate.line'].create([
            {
                'certificate_id': certificate.id,
                'description': 'Earthwork',
                'previous_quantity': 0.0,
                'current_quantity': 100.0,
                'unit_price': 10.0,
            },
            {
                'certificate_id': certificate.id,
                'description': 'Concrete',
                'previous_quantity': 0.0,
                'current_quantity': 50.0,
                'unit_price': 40.0,
            },
        ])
        current = 100.0 * 10.0 + 50.0 * 40.0
        self.assertEqual(certificate.current_amount, current)
        self.assertEqual(certificate.retention_amount, current * 0.10)
        self.assertEqual(certificate.net_amount, current * 0.90)
        self.assertEqual(certificate.amount_to_pay, current * 0.90)
        certificate.action_confirm()
        self.assertEqual(certificate.state, 'confirmed')
        certificate.action_paid()
        self.assertEqual(certificate.state, 'paid')

    def test_certificate_period_validation(self):
        subcontract = self.env['construction.subcontract'].create({
            'project_id': self.project.id,
            'contractor_id': self.contractor.id,
            'retention_rate': 10.0,
        })
        with self.assertRaises(UserError):
            self.env['construction.payment.certificate'].create({
                'subcontract_id': subcontract.id,
                'project_id': self.project.id,
                'contractor_id': self.contractor.id,
                'period_start': '2026-02-01',
                'period_end': '2026-01-31',
            })

    def test_create_certificate_from_subcontract(self):
        subcontract = self.env['construction.subcontract'].create({
            'project_id': self.project.id,
            'contractor_id': self.contractor.id,
            'retention_rate': 5.0,
        })
        subcontract.action_confirm()
        action = subcontract.action_create_certificate()
        certificate = self.env['construction.payment.certificate'].browse(action['res_id'])
        self.assertTrue(certificate)
        self.assertEqual(certificate.subcontract_id, subcontract)
        self.assertEqual(certificate.retention_rate, 5.0)