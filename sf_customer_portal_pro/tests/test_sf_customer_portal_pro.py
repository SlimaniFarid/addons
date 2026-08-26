# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfCustomerPortalPro(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        portal = self.env['customer.portal.config'].create({
            'name': 'Test Portal',
        })
        self.assertTrue(portal.name)

    def test_workflow(self):
        config = self.env['customer.portal.config'].create({
            'name': 'Test Portal',
            'state': 'draft',
        })
        self.assertEqual(config.state, 'draft')