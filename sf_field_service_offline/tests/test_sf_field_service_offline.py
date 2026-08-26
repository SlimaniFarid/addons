# -*- coding: utf-8 -*-
import uuid
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestSfFieldServiceOffline(TransactionCase):

    def setUp(self):
        super().setUp()
        self.customer = self.env['res.partner'].create({
            'name': 'Customer %s' % uuid.uuid4().hex[:6],
        })

    def test_sequences(self):
        task = self.env['fsoffline.task'].create({
            'name': 'Test Task',
        })
        self.assertTrue(task.name.startswith('FSO-'))

    def test_workflow(self):
        task = self.env['fsoffline.task'].create({
            'name': 'Test Task',
            'state': 'draft',
        })
        self.assertEqual(task.state, 'draft')