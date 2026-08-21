# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfReturnsRma(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        rma = self.env['sf.returns.rma'].create({
            'name': 'Test RMA',
        })
        self.assertTrue(rma.name.startswith('RMA-'))

    def test_workflow(self):
        rma = self.env['sf.returns.rma'].create({
            'name': 'Test RMA',
            'state': 'draft',
        })
        self.assertEqual(rma.state, 'draft')