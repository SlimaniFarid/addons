# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfRevenueRecognition(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        revrec = self.env['revrec.contract'].create({
            'name': 'Test Revenue Contract',
        })
        self.assertTrue(revrec.name.startswith('REV-'))

    def test_workflow(self):
        revrec = self.env['revrec.contract'].create({
            'name': 'Test Revenue Contract',
            'state': 'draft',
        })
        self.assertEqual(revrec.state, 'draft')