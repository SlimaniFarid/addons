# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfAiContractAnalyzer(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        doc = self.env['contract.document'].create({
            'name': 'Test Contract',
            'contract_type': 'sales',
        })
        self.assertTrue(doc.name.startswith('CD-'))

    def test_document_workflow(self):
        doc = self.env['contract.document'].create({
            'name': 'Test Contract',
            'contract_type': 'sales',
            'state': 'draft',
        })
        self.assertEqual(doc.state, 'draft')