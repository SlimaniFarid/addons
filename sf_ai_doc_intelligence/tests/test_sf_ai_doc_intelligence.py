# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfAiDocIntelligence(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        doc = self.env['docintel.document'].create({
            'name': 'Test Document',
        })
        self.assertTrue(doc.name.startswith('DIN-'))

    def test_document_workflow(self):
        doc = self.env['docintel.document'].create({
            'name': 'Test Document',
            'state': 'draft',
        })
        self.assertEqual(doc.state, 'draft')