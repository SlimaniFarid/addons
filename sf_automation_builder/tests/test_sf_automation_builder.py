# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfAutomationBuilder(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        auto = self.env['automation.rule'].create({
            'name': 'Test Automation',
        })
        self.assertTrue(auto.name.startswith('AUT-'))

    def test_workflow(self):
        auto = self.env['automation.rule'].create({
            'name': 'Test Automation',
            'state': 'draft',
        })
        self.assertEqual(auto.state, 'draft')