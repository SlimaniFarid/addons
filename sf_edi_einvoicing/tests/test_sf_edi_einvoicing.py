# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfEdiEinvoicing(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        config = self.env['edi.config'].create({
            'name': 'Test EDI Config',
        })
        self.assertTrue(config.name)

    def test_workflow(self):
        config = self.env['edi.config'].create({
            'name': 'Test EDI Config',
            'state': 'draft',
        })
        self.assertEqual(config.state, 'draft')