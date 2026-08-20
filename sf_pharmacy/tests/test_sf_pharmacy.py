# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import fields
from odoo.exceptions import AccessError, UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfPharmacy(TransactionCase):

    def setUp(self):
        super(TestSfPharmacy, self).setUp()
        self.base_user = self.env.ref('base.group_user')
        self.user_group = self.env.ref('sf_pharmacy.group_sf_pharmacy_user')
        self.manager_group = self.env.ref('sf_pharmacy.group_sf_pharmacy_manager')
        self.company1 = self.env.company
        self.company2 = self.env['res.company'].create({'name': 'Pharma Test 2'})
        self.user = self._create_user('u_pharma', [self.user_group.id])
        self.manager = self._create_user('m_pharma', [self.user_group.id, self.manager_group.id])

    def _create_user(self, login, group_ids, company_ids=None):
        company_ids = company_ids or [self.company1.id, self.company2.id]
        return self.env['res.users'].create({
            'name': login.title(),
            'login': login,
            'groups_id': [(6, 0, [self.base_user.id] + group_ids)],
            'company_id': self.company1.id,
            'company_ids': [(6, 0, company_ids)],
        })

    def _create_product(self, name='Amoxicilline 500 mg'):
        return self.env['sf.pharmacy.product'].with_user(self.manager).create({
            'name': name,
            'form': 'comprime',
            'price_unit': 5.0,
            'cost': 2.0,
            'safety_stock': 5.0,
        })

    def _receive(self, product, qty, expiry_days=365, company=None):
        company = company or self.company1
        batch = self.env['sf.pharmacy.batch'].with_user(self.manager).with_company(company).create({
            'product_id': product.id,
            'expiry_date': fields.Date.today() + timedelta(days=expiry_days),
            'company_id': company.id,
        })
        self.env['sf.pharmacy.batch_movement'].with_user(self.manager).with_company(company).create({
            'batch_id': batch.id,
            'movement_type': 'in',
            'qty': qty,
            'company_id': company.id,
        })
        return batch

    def _create_prescription(self, patient='Test Patient', prescriber='Dr Martin'):
        return self.env['sf.pharmacy.prescription'].with_user(self.manager).create({
            'patient_name': patient,
            'prescriber': prescriber,
        })

    def _create_dispensation(self, prescription, product, batch, qty=5.0, posology='1 boîte x 2/j'):
        return self.env['sf.pharmacy.dispensation'].with_user(self.manager).create({
            'prescription_id': prescription.id,
            'product_id': product.id,
            'batch_id': batch.id,
            'qty': qty,
            'posology': posology,
        })

    def test_sequence_prefixes(self):
        product = self._create_product()
        self.assertTrue(product.name.startswith('PRE-'))
        batch = self._receive(product, 10)
        self.assertTrue(batch.name.startswith('BAT-'))
        prescription = self._create_prescription()
        self.assertTrue(prescription.name.startswith('ORD-'))
        dispensation = self._create_dispensation(prescription, product, batch, qty=2.0)
        self.assertTrue(dispensation.name.startswith('DEL-'))
        movement = self.env['sf.pharmacy.batch_movement'].with_user(self.manager).create({
            'batch_id': batch.id,
            'movement_type': 'adjustment',
            'qty': 1.0,
            'company_id': self.company1.id,
        })
        self.assertTrue(movement.name.startswith('MVT-'))

    def test_qty_available_flow(self):
        product = self._create_product()
        batch = self._receive(product, 10)
        self.assertEqual(batch.qty_available, 10.0)
        prescription = self._create_prescription()
        dispensation = self._create_dispensation(prescription, product, batch, qty=3.0)
        prescription.action_confirm()
        prescription.action_done()
        self.assertEqual(batch.qty_dispensed, 3.0)
        self.assertEqual(batch.qty_available, 7.0)
        self.env['sf.pharmacy.batch_movement'].with_user(self.manager).create({
            'batch_id': batch.id,
            'movement_type': 'adjustment',
            'qty': 2.0,
            'company_id': self.company1.id,
        })
        self.assertEqual(batch.qty_available, 9.0)
        batch.with_user(self.manager).write({'qty_reserved': 2.0})
        self.assertEqual(batch.qty_available, 7.0)

    def test_dispensation_insufficient_stock(self):
        product = self._create_product()
        batch = self._receive(product, 5)
        prescription = self._create_prescription()
        with self.assertRaises(UserError):
            self._create_dispensation(prescription, product, batch, qty=10.0)

    def test_dispensation_expired_lot(self):
        product = self._create_product()
        batch = self._receive(product, 10, expiry_days=-1)
        self.assertEqual(batch.status, 'expired')
        prescription = self._create_prescription()
        with self.assertRaises(UserError):
            self._create_dispensation(prescription, product, batch, qty=2.0)

    def test_dispensation_withdrawn_lot(self):
        product = self._create_product()
        batch = self._receive(product, 10)
        batch.with_user(self.manager).action_withdraw()
        self.assertEqual(batch.status, 'withdrawn')
        self.assertEqual(batch.qty_available, 0.0)
        prescription = self._create_prescription()
        with self.assertRaises(UserError):
            self._create_dispensation(prescription, product, batch, qty=2.0)

    def test_negative_stock_impossible(self):
        product = self._create_product()
        batch = self._receive(product, 10)
        with self.assertRaises(UserError):
            self.env['sf.pharmacy.batch_movement'].with_user(self.manager).create({
                'batch_id': batch.id,
                'movement_type': 'adjustment',
                'qty': -100.0,
                'company_id': self.company1.id,
            })
        with self.assertRaises(UserError):
            self.env['sf.pharmacy.batch_movement'].with_user(self.manager).create({
                'batch_id': batch.id,
                'movement_type': 'out',
                'qty': 50.0,
                'company_id': self.company1.id,
            })

    def test_manager_only_actions(self):
        product = self._create_product()
        batch = self._receive(product, 10)
        with self.assertRaises(AccessError):
            batch.with_user(self.user).action_withdraw()
        with self.assertRaises(AccessError):
            batch.with_user(self.user).action_recall()
        with self.assertRaises(AccessError):
            self.env['sf.pharmacy.batch_movement'].with_user(self.user).create({
                'batch_id': batch.id,
                'movement_type': 'adjustment',
                'qty': 1.0,
                'company_id': self.company1.id,
            })
        batch.with_user(self.manager).action_withdraw()
        self.assertEqual(batch.status, 'withdrawn')
        self.assertEqual(batch.qty_available, 0.0)

    def test_fifo_batch_selection(self):
        product = self._create_product()
        batch_late = self._receive(product, 10, expiry_days=60)
        batch_near = self._receive(product, 10, expiry_days=30)
        prescription = self._create_prescription()
        dispensation = self.env['sf.pharmacy.dispensation'].with_user(self.manager).create({
            'prescription_id': prescription.id,
            'product_id': product.id,
            'qty': 1.0,
        })
        self.assertEqual(dispensation.batch_id.id, batch_near.id)
        self.assertNotEqual(dispensation.batch_id.id, batch_late.id)

    def test_cron_alerts_dedup(self):
        icp = self.env['ir.config_parameter'].sudo()
        icp.set_param('sf_pharmacy.expiry_days', '90')
        icp.set_param('sf_pharmacy.low_stock_threshold', '5.0')
        product = self._create_product()
        batch = self._receive(product, 100, expiry_days=10)
        self.env['sf.pharmacy.batch']._cron_stock_alerts()
        self.env['sf.pharmacy.batch']._cron_stock_alerts()
        activities = self.env['mail.activity'].search([
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id),
            ('res_model', '=', 'sf.pharmacy.batch'),
            ('res_id', '=', batch.id),
        ])
        self.assertEqual(len(activities), 1)

    def test_cron_multi_company(self):
        icp = self.env['ir.config_parameter'].sudo()
        icp.set_param('sf_pharmacy.expiry_days', '90')
        product = self._create_product()
        batch1 = self._receive(product, 100, expiry_days=10, company=self.company1)
        batch2 = self._receive(product, 100, expiry_days=10, company=self.company2)
        self.env['sf.pharmacy.batch']._cron_stock_alerts()
        for batch in (batch1, batch2):
            self.assertTrue(self.env['mail.activity'].search([
                ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id),
                ('res_model', '=', 'sf.pharmacy.batch'),
                ('res_id', '=', batch.id),
            ]))

    def test_multi_company_rule(self):
        product = self._create_product()
        batch1 = self._receive(product, 10, company=self.company1)
        batch2 = self._receive(product, 10, company=self.company2)
        user_c1 = self._create_user('u_c1', [self.user_group.id], company_ids=[self.company1.id])
        visible = self.env['sf.pharmacy.batch'].with_user(user_c1).search([('product_id', '=', product.id)])
        self.assertIn(batch1.id, visible.ids)
        self.assertNotIn(batch2.id, visible.ids)
        manager_visible = self.env['sf.pharmacy.batch'].with_user(self.manager).search([('product_id', '=', product.id)])
        self.assertEqual(set(manager_visible.ids), set([batch1.id, batch2.id]))

    def test_prescription_flow(self):
        product = self._create_product()
        batch = self._receive(product, 20)
        prescription = self._create_prescription()
        dispensation = self._create_dispensation(prescription, product, batch, qty=5.0)
        prescription.action_confirm()
        self.assertEqual(prescription.state, 'confirmed')
        prescription.action_done()
        self.assertEqual(prescription.state, 'done')
        self.assertEqual(dispensation.state, 'done')
        self.assertTrue(dispensation.dispensed_at)
        self.assertTrue(dispensation.dispensed_by)
        self.assertEqual(batch.qty_dispensed, 5.0)

    def test_prescription_confirm_blocks_unsold(self):
        product = self._create_product()
        batch = self._receive(product, 20)
        prescription = self._create_prescription()
        self.env['sf.pharmacy.dispensation'].with_user(self.manager).create({
            'prescription_id': prescription.id,
            'product_id': product.id,
            'batch_id': batch.id,
            'qty': 0.0,
        })
        with self.assertRaises(UserError):
            prescription.action_confirm()

    def test_reports_generate(self):
        product = self._create_product()
        batch = self._receive(product, 20, expiry_days=120)
        prescription = self._create_prescription()
        dispensation = self._create_dispensation(prescription, product, batch, qty=5.0)
        prescription.action_confirm()
        prescription.action_done()
        report_inventory = self.env.ref('sf_pharmacy.sf_pharmacy_action_report_inventory')
        pdf, _ = report_inventory._render_qweb_pdf(batch.ids)
        self.assertTrue(pdf.startswith(b'%PDF'))
        report_deliveries = self.env.ref('sf_pharmacy.sf_pharmacy_action_report_deliveries')
        pdf, _ = report_deliveries._render_qweb_pdf(dispensation.ids)
        self.assertTrue(pdf.startswith(b'%PDF'))
        report_value = self.env.ref('sf_pharmacy.sf_pharmacy_action_report_stock_value')
        pdf, _ = report_value._render_qweb_pdf(product.ids)
        self.assertTrue(pdf.startswith(b'%PDF'))