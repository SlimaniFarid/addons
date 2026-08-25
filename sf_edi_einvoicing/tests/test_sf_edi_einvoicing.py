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

    def test_peppol_participant_registration(self):
        """Test Peppol participant registration action"""
        config = self.env['edi.peppol.config'].create({
            'name': 'Test Peppol Config',
            'participant_id': '0192:123456789',
            'participant_scheme': '0192',
        })
        result = config.action_register_participant()
        self.assertEqual(result['type'], 'ir.actions.client')
        self.assertEqual(result['params']['type'], 'info')
        self.assertIn('0192:123456789', result['params']['message'])