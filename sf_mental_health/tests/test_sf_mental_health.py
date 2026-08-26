# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged

@tagged('post_install', '-at_install')
class TestSfmentalhealth(TransactionCase):
    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({'name': 'Customer %s' % uuid.uuid4().hex[:6]})

    def test_sequences(self):
        record = self.env['sf_mental_health'].create({})
        self.assertTrue(record.name)

    def test_workflow(self):
        record = self.env['sf_mental_health'].create({})
        self.assertEqual(record.state, 'draft')
