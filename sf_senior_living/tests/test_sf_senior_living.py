# -*- coding: utf-8 -*-
import uuid
from datetime import datetime, timedelta

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfseniorliving(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })
        self.company = self.env.company

    def _create_sfseniorliving(self, **kwargs):
        return self.env['sf.senior.residence'].create(kwargs)

    def test_sequences(self):
        record = self._create_sfseniorliving()
        self.assertTrue(record.name.startswith('RES--'))

    def test_workflow(self):
        record = self._create_sfseniorliving()
        # Test basic workflow
        self.assertEqual(record.state, 'draft')

    def test_report_generation(self):
        record = self._create_sfseniorliving()
        for report in [{'action_id': 'action_report_resident_invoice', 'name': 'Resident Invoice', 'model': 'sf.senior.resident', 'report_name': 'sf_senior_living.report_resident_invoice', 'report_file': 'sf_senior_living.report_resident_invoice', 'model_ref': 'model_sf_senior_living_resident', 'template_id': 'report_resident_invoice_template', 'template_file': 'report_resident_invoice'}]:
            action = self.env.ref('sf_senior_living.' + report['action_id']).report_action(record)
            self.assertTrue(action)

    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Test Company 2'})
        record1 = self._create_sfseniorliving()
        record2 = self.env['sf.senior.residence'].with_company(company2).create({
            'company_id': company2.id,
        })
        user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'user_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [self.env.ref('sf_senior_living.group_sf_senior_living_user').id])],
            'company_ids': [(6, 0, [self.env.company.id])],
        })
        self.assertTrue(record1.with_user(user).exists())
        self.assertFalse(record2.with_user(user).exists())

