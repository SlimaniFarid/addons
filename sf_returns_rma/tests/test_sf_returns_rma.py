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
        self.product = self.env['product.product'].create({
            'name': 'Test Product',
            'type': 'consu',
        })
        self.warehouse = self.env['stock.warehouse'].search([], limit=1)

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

    def test_disposition_repair(self):
        """Test RMA disposition repair action creates repair order"""
        rma = self.env['sf.returns.rma'].create({
            'name': 'Test RMA Repair',
            'partner_id': self.customer.id,
            'line_ids': [(0, 0, {'product_id': self.product.id, 'quantity': 1})],
        })
        disposition = self.env['rma.disposition'].create({
            'rma_id': rma.id,
            'action': 'repair',
        })
        disposition.action_execute()
        self.assertTrue(disposition.repair_order_id)
        self.assertEqual(disposition.repair_order_id.product_id, self.product)

    def test_disposition_scrap(self):
        """Test RMA disposition scrap action creates scrap move"""
        rma = self.env['sf.returns.rma'].create({
            'name': 'Test RMA Scrap',
            'partner_id': self.customer.id,
            'line_ids': [(0, 0, {'product_id': self.product.id, 'quantity': 1})],
        })
        disposition = self.env['rma.disposition'].create({
            'rma_id': rma.id,
            'action': 'scrap',
            'scrap_reason': 'Defective',
        })
        disposition.action_execute()
        # Check scrap was created
        scrap = self.env['stock.scrap'].search([('origin', '=', rma.name)])
        self.assertTrue(scrap)
        self.assertEqual(scrap.product_id, self.product)