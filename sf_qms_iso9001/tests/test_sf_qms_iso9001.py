# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfQmsIso9001(TransactionCase):

    def setUp(self):
        super().setUp()
        self.user = self.env['res.users'].create({
            'name': 'Test User',
            'login': 'test_user_%s' % uuid.uuid4().hex[:6],
            'email': 'test@example.com',
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

    def test_document_distribution_notify(self):
        """Test document distribution notification on publish"""
        doc = self.env['qms.document'].create({
            'name': 'Test Document',
            'code': 'DOC-001',
            'category': 'procedure',
            'version': '1.0',
            'state': 'approved',
            'distribution_ids': [(0, 0, {'user_id': self.user.id, 'role': 'reader'})],
        })
        # Mock the activity creation to avoid issues in test
        doc.action_publish()
        self.assertEqual(doc.state, 'published')
        # Check that message was posted
        messages = doc.message_ids.filtered(lambda m: 'published' in m.body)
        self.assertTrue(messages)