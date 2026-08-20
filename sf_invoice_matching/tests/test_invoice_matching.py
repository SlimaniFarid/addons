# -*- coding: utf-8 -*-
from odoo import fields
from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestInvoiceMatching(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Move = self.env['account.move']
        self.MatchLine = self.env['sf.invoice.match.line']
        self.Exception = self.env['sf.invoice.exception']
        self.group_user = self.env.ref(
            'sf_invoice_matching.group_invoice_matching_user')
        self.group_manager = self.env.ref(
            'sf_invoice_matching.group_invoice_matching_manager')
        self.env.user.groups_id += self.group_manager

    def _create_partner(self):
        return self.env['res.partner'].create({'name': 'Supplier'})

    def _create_journal(self):
        return self.env['account.journal'].create({
            'name': 'Vendor Bills Test',
            'type': 'purchase',
            'code': 'SFPUR',
        })

    def _create_product(self):
        return self.env['product.product'].create({
            'name': 'Test Item',
            'type': 'product',
        })

    def _receive_po(self, po, qty=10.0):
        for picking in po.picking_ids:
            for move in picking.move_ids_without_package:
                move.quantity = qty
                move.picked = True
            picking.button_validate()

    def _create_bill(self, partner, journal, qty=10.0, price=10.0):
        return self.Move.create({
            'move_type': 'in_invoice',
            'partner_id': partner.id,
            'journal_id': journal.id,
            'invoice_date': fields.Date.today(),
            'invoice_line_ids': [(0, 0, {
                'name': 'Test Line',
                'quantity': qty,
                'price_unit': price,
            })],
        })

    def _create_po(self, product, partner, qty=10.0, price=10.0):
        po = self.env['purchase.order'].create({
            'partner_id': partner.id,
            'order_line': [(0, 0, {
                'product_id': product.id,
                'product_qty': qty,
                'price_unit': price,
            })],
        })
        po.button_confirm()
        return po

    def test_match_line_ok(self):
        partner = self._create_partner()
        journal = self._create_journal()
        bill = self._create_bill(partner, journal)
        line = self.MatchLine.create({
            'move_id': bill.id,
            'qty_invoice': 10.0,
            'qty_received': 10.0,
            'qty_ordered': 10.0,
            'price_invoice': 10.0,
            'price_ordered': 10.0,
        })
        self.assertEqual(line.status, 'ok')
        self.assertEqual(line.qty_diff, 0.0)
        self.assertEqual(line.price_diff_pct, 0.0)

    def test_match_line_major(self):
        partner = self._create_partner()
        journal = self._create_journal()
        bill = self._create_bill(partner, journal)
        line = self.MatchLine.create({
            'move_id': bill.id,
            'qty_invoice': 10.0,
            'qty_received': 10.0,
            'qty_ordered': 10.0,
            'price_invoice': 12.0,
            'price_ordered': 10.0,
        })
        self.assertEqual(line.status, 'major')
        self.assertAlmostEqual(line.price_diff_pct, 20.0, places=1)

    def test_match_line_minor(self):
        partner = self._create_partner()
        partner.sf_match_tolerance_qty = 1.0
        journal = self._create_journal()
        bill = self._create_bill(partner, journal)
        line = self.MatchLine.create({
            'move_id': bill.id,
            'qty_invoice': 10.0,
            'qty_received': 9.8,
            'qty_ordered': 10.0,
            'price_invoice': 10.0,
            'price_ordered': 10.0,
        })
        self.assertEqual(line.status, 'minor')

    def test_run_match_matched(self):
        partner = self._create_partner()
        journal = self._create_journal()
        product = self._create_product()
        po = self._create_po(product, partner, qty=10.0, price=10.0)
        self._receive_po(po)
        bill = self._create_bill(partner, journal, qty=10.0, price=10.0)
        po_line = po.order_line[0]
        bill.invoice_line_ids[0].purchase_line_id = po_line.id
        bill.action_run_match()
        self.assertEqual(bill.sf_match_state, 'matched')

    def test_run_match_major_blocks_payment(self):
        partner = self._create_partner()
        journal = self._create_journal()
        product = self._create_product()
        po = self._create_po(product, partner, qty=10.0, price=10.0)
        self._receive_po(po)
        bill = self._create_bill(partner, journal, qty=10.0, price=10.5)
        po_line = po.order_line[0]
        bill.invoice_line_ids[0].purchase_line_id = po_line.id
        bill.action_run_match()
        self.assertEqual(bill.sf_match_state, 'exception')
        self.assertTrue(bill.sf_has_major_discrepancy)
        self.assertTrue(bill._sf_has_open_major_exception())
        with self.assertRaises(UserError):
            bill.action_post()

    def test_arbitrate_accept_resolves(self):
        partner = self._create_partner()
        journal = self._create_journal()
        product = self._create_product()
        po = self._create_po(product, partner, qty=10.0, price=10.0)
        self._receive_po(po)
        bill = self._create_bill(partner, journal, qty=10.0, price=10.5)
        po_line = po.order_line[0]
        bill.invoice_line_ids[0].purchase_line_id = po_line.id
        bill.action_run_match()
        exception = bill.sf_match_exception_ids[0]
        wizard = self.env['sf.invoice.exception.wizard'].create({
            'exception_id': exception.id,
            'decision': 'accept',
            'responsible_id': self.env.user.id,
            'decision_note': 'Price agreed with supplier.',
        })
        wizard.action_confirm()
        self.assertEqual(exception.state, 'arbitrated')
        self.assertEqual(bill.sf_match_state, 'resolved')
        self.assertFalse(bill._sf_has_open_major_exception())

    def test_arbitrate_revise_keeps_blocked(self):
        partner = self._create_partner()
        journal = self._create_journal()
        product = self._create_product()
        po = self._create_po(product, partner, qty=10.0, price=10.0)
        self._receive_po(po)
        bill = self._create_bill(partner, journal, qty=10.0, price=10.5)
        po_line = po.order_line[0]
        bill.invoice_line_ids[0].purchase_line_id = po_line.id
        bill.action_run_match()
        exception = bill.sf_match_exception_ids[0]
        wizard = self.env['sf.invoice.exception.wizard'].create({
            'exception_id': exception.id,
            'decision': 'revise',
            'decision_note': 'Ask supplier to reissue.',
        })
        wizard.action_confirm()
        self.assertEqual(exception.state, 'rejected')
        self.assertEqual(bill.sf_match_state, 'exception')
        self.assertTrue(bill._sf_has_open_major_exception())

    def test_supplier_tolerance_used(self):
        partner = self._create_partner()
        partner.sf_match_tolerance_price_pct = 10.0
        partner.sf_match_tolerance_total_pct = 10.0
        journal = self._create_journal()
        product = self._create_product()
        po = self._create_po(product, partner, qty=10.0, price=10.0)
        self._receive_po(po)
        bill = self._create_bill(partner, journal, qty=10.0, price=10.5)
        po_line = po.order_line[0]
        bill.invoice_line_ids[0].purchase_line_id = po_line.id
        bill.action_run_match()
        self.assertEqual(bill.sf_match_state, 'matched')

    def test_multi_company_rule(self):
        company_b = self.env['res.company'].create({'name': 'Match Company B'})
        user = self.env['res.users'].create({
            'name': 'Match Company A User',
            'login': 'match_company_a_user',
            'groups_id': [(4, self.group_user.id)],
        })
        partner = self._create_partner()
        journal = self._create_journal()
        bill = self.Move.with_company(company_b).create({
            'move_type': 'in_invoice',
            'partner_id': partner.id,
            'journal_id': journal.id,
            'invoice_line_ids': [(0, 0, {
                'name': 'Test Line',
                'quantity': 10.0,
                'price_unit': 10.0,
            })],
        })
        exception = self.Exception.create({
            'move_id': bill.id,
            'severity': 'major',
            'description': 'Test',
        })
        self.assertEqual(exception.company_id, company_b)
        self.assertNotIn(exception, self.Exception.with_user(user).search(
            [('id', '=', exception.id)]))