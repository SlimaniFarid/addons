# -*- coding: utf-8 -*-
"""Unit tests for Wave2/F engines. Run under odoo-bin --test-enable."""
from datetime import timedelta

from odoo import fields
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestOeeEngine(TransactionCase):

    def test_oee_reference_case(self):
        """Availability 80% x Performance 100% x Quality 95% = 76%."""
        wc = self.env['mrp.workcenter'].create({'name': 'WC-T'})
        rec = self.env['sf.production_oee_calculator'].create({
            'name': 'OEE-TEST',
            'workcenter_id': wc.id,
            'planned_time': 10.0,
            'downtime': 2.0,
            'ideal_cycle': 0.05,
            'total_count': 160,
            'good_count': 152,
        })
        rec._compute_oee()
        # availability .8, performance 160*.05/8=1.0, quality .95
        self.assertAlmostEqual(rec.oee_percent, 0.8 * 1.0 * 0.95 * 100,
                               places=2)

    def test_oee_zero_planned(self):
        wc = self.env['mrp.workcenter'].create({'name': 'WC-Z'})
        rec = self.env['sf.production_oee_calculator'].create({
            'name': 'OEE-ZERO', 'workcenter_id': wc.id})
        rec._compute_oee()
        self.assertEqual(rec.oee_percent, 0.0)


@tagged('post_install', '-at_install')
class TestLateInterest(TransactionCase):

    def _mk_invoice(self, due_offset_days, residual=1000.0):
        partner = self.env['res.partner'].create({'name': 'LP-Cust'})
        move = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': partner.id,
            'invoice_date': fields.Date.context_today(self)
            - timedelta(days=due_offset_days + 30),
            'invoice_date_due': fields.Date.context_today(self)
            - timedelta(days=due_offset_days),
        })
        self.env['account.move.line'].create({
            'move_id': move.id,
            'name': 'line',
            'quantity': 1,
            'price_unit': residual,
            'account_id': self.env['account.account'].search(
                [('account_type', '=', 'asset_receivable')], limit=1).id,
        })
        move.action_post()
        return move

    def test_interest_formula(self):
        inv = self._mk_invoice(due_offset_days=40)
        inv.amount_residual  # ensure computed
        run = self.env['sf.late.interest'].create({
            'name': 'LPI-TEST', 'rate_percent': 5.0, 'grace_days': 10,
        })
        run.as_of_date = fields.Date.context_today(run)
        run.action_compute()
        line = run.line_ids.filtered(
            lambda l: l.invoice_id == inv)
        self.assertTrue(line)
        expected = round(1000.0 * 0.05 * (40 - 10) / 365.0, 2)
        self.assertAlmostEqual(line.interest_amount, expected, places=2)

    def test_grace_exclusion(self):
        inv = self._mk_invoice(due_offset_days=5)
        run = self.env['sf.late.interest'].create({
            'name': 'LPI-GRACE', 'rate_percent': 10.0, 'grace_days': 30,
        })
        run.action_compute()
        self.assertFalse(run.line_ids.filtered(
            lambda l: l.invoice_id == inv))


@tagged('post_install', '-at_install')
class TestSegmentsRFM(TransactionCase):

    def test_rfm_member_count(self):
        partner = self.env['res.partner'].create({'name': 'RFM-Cust'})
        product = self.env['product.product'].create({'name': 'P'})
        for _ in range(2):
            so = self.env['sale.order'].create({
                'partner_id': partner.id,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'product_uom_qty': 1,
                    'price_unit': 500.0,
                })],
            })
            so.action_confirm()
        seg = self.env['sf.customer_segments_rules'].create({
            'segment_name': 'Gold',
            'recency_max_days': 30,
            'frequency_min': 2,
            'monetary_min': 500.0,
        })
        seg.action_refresh_members()
        self.assertEqual(seg.member_count, 1)

    def test_rfm_frequency_filter(self):
        seg = self.env['sf.customer_segments_rules'].create({
            'segment_name': 'VIP', 'frequency_min': 99,
        })
        seg.action_refresh_members()
        self.assertEqual(seg.member_count, 0)


@tagged('post_install', '-at_install')
class TestMinMaxUsage(TransactionCase):

    def test_proposal_monotonic(self):
        product = self.env['product.product'].create({'name': 'MM-P'})
        loc_customer = self.env.ref('stock.stock_location_customers')
        loc_stock = self.env.ref('stock.stock_location_stock')
        for qty in (3, 5, 4):
            self.env['stock.move'].create({
                'name': 'out',
                'product_id': product.id,
                'product_uom_qty': qty,
                'product_uom': product.uom_id.id,
                'location_id': loc_stock.id,
                'location_dest_id': loc_customer.id,
            })._action_done()
        rec = self.env['sf.minmax_review'].create({
            'product_id': product.id,
            'cover_days_min': 7,
            'cover_days_max': 30,
        })
        rec.action_propose_from_usage()
        self.assertGreaterEqual(rec.proposed_max, rec.proposed_min)
        self.assertGreater(rec.proposed_min, 0)
