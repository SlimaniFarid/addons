# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfQmsIso9001(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        audit = self.env['qms.audit'].create({
            'name': 'Test Audit',
        })
        self.assertTrue(audit.name.startswith('AUD-'))

    def test_workflow(self):
        audit = self.env['qms.audit'].create({
            'name': 'Test Audit',
            'state': 'draft',
        })
        self.assertEqual(audit.state, 'draft')