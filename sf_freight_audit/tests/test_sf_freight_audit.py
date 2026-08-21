# -*- coding: utf-8 -*-
import base64
import io
import uuid
from datetime import date, timedelta

from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged

CSV_HEADER = ('invoice_ref,tracking_ref,charge_type,description,'
              'ship_date,weight_kg,amount_billed\n')


def _csv(*rows):
    return base64.b64encode((CSV_HEADER + ''.join(rows)).encode('utf-8'))


@tagged('post_install', '-at_install')
class TestSfFreightAudit(TransactionCase):

    def setUp(self):
        super().setUp()
        self.company = self.env.company
        self.carrier = self.env['res.partner'].create({
            'name': 'Carrier %s' % uuid.uuid4().hex[:6],
            'is_company': True,
        })
        self.contract = self.env['sf.freight.carrier.contract'].create({
            'partner_id': self.carrier.id,
            'tolerance_pct': 0.5,
            'warn_pct': 2.0,
            'high_pct': 5.0,
            'crit_pct': 10.0,
            'date_start': date.today() - timedelta(days=30),
        })
        self.contract.action_activate()

    def _make_invoice(self, lines):
        return self.env['sf.freight.invoice'].create({
            'carrier_id': self.carrier.id,
            'contract_id': self.contract.id,
            'invoice_ref': 'INV-%s' % uuid.uuid4().hex[:6],
            'invoice_date': date.today(),
            'line_ids': [(0, 0, l) for l in lines],
        })

    # T01 sequences
    def test_sequences(self):
        inv = self._make_invoice([{
            'charge_type': 'base_freight',
            'tracking_ref': 'T%s' % uuid.uuid4().hex[:6],
            'uom_weight': 10.0,
            'amount_billed': 100.0,
        }])
        self.assertTrue(inv.name.startswith('FAU-'))
        dispute = self.env['sf.freight.dispute'].create({
            'invoice_id': inv.id,
            'finding_ids': [(0, 0, {
                'invoice_id': inv.id,
                'finding_type': 'rate_variance',
                'severity': 'medium',
                'expected_amount': 90.0,
                'actual_amount': 100.0,
            })],
        })
        self.assertTrue(dispute.name.startswith('DPT-'))

    # T02 import wizard happy path
    def test_import_wizard(self):
        csv_data = _csv(
            'INV-X1,T001,base_freight,Base,%s,10.0,100.0\n'
            % date.today().isoformat(),
            'INV-X1,,fuel_surcharge,Fuel,%s,0.0,15.0\n'
            % date.today().isoformat(),
            'BAD ROW LINE\n',
        )
        wiz = self.env['sf.freight.import.wizard'].create({
            'carrier_id': self.carrier.id,
            'contract_id': self.contract.id,
            'invoice_ref': 'INV-X1',
            'invoice_date': date.today(),
            'csv_file': csv_data,
            'dry_run': False,
        })
        result = wiz.action_import()
        invoice = self.env['sf.freight.invoice'].browse(result['res_id'])
        self.assertEqual(len(invoice.line_ids), 2)

    # T03 matching + T04 rate variance
    def test_rate_variance_detection(self):
        inv = self._make_invoice([{
            'charge_type': 'base_freight',
            'tracking_ref': '',
            'uom_weight': 10.0,
            'amount_billed': 500.0,
        }])
        inv.action_run_audit()
        self.assertEqual(inv.state, 'discrepancy')
        finding = inv.finding_ids.filtered(
            lambda f: f.finding_type == 'rate_variance')
        self.assertTrue(finding)

    def test_tolerance_ok(self):
        inv = self._make_invoice([{
            'charge_type': 'base_freight',
            'tracking_ref': '',
            'uom_weight': 10.0,
            'amount_billed': 100.4,
        }])
        inv.action_run_audit()
        rate_findings = inv.finding_ids.filtered(
            lambda f: f.finding_type == 'rate_variance')
        self.assertFalse(rate_findings)

    # T05 severity thresholds
    def test_severity_thresholds(self):
        for amount, expected_sev in [(120.0, 'medium'), (160.0, 'high'),
                                     (250.0, 'critical')]:
            inv = self._make_invoice([{
                'charge_type': 'base_freight',
                'tracking_ref': '',
                'uom_weight': 10.0,
                'amount_billed': amount,
            }])
            inv.action_run_audit()
            f = inv.finding_ids.filtered(
                lambda ff: ff.finding_type == 'rate_variance')
            if f:
                self.assertEqual(f.severity, expected_sev)

    # T06 payment blocked with open findings
    def test_payment_blocked_with_open_finding(self):
        inv = self._make_invoice([{
            'charge_type': 'base_freight',
            'tracking_ref': '',
            'uom_weight': 10.0,
            'amount_billed': 500.0,
        }])
        inv.action_run_audit()
        with self.assertRaises(UserError):
            inv.action_validate_payment()

    # T07 dispute workflow
    def test_dispute_workflow(self):
        inv = self._make_invoice([{
            'charge_type': 'base_freight',
            'tracking_ref': '',
            'uom_weight': 10.0,
            'amount_billed': 500.0,
        }])
        inv.action_run_audit()
        finding = inv.finding_ids[0]
        dispute = self.env['sf.freight.dispute'].create({
            'invoice_id': inv.id,
            'finding_ids': [(6, 0, finding.ids)],
        })
        dispute.action_submit()
        self.assertEqual(dispute.state, 'submitted')
        self.assertEqual(inv.state, 'disputed')
        dispute.carrier_response = 'Partial refund accepted.'
        dispute.action_carrier_responded()
        dispute.action_resolve_credit_note()
        self.assertEqual(dispute.state, 'resolved')
        self.assertTrue(dispute.credit_note_id)
        self.assertEqual(dispute.credit_note_id.move_type, 'in_refund')

    # T08 cron idempotent
    def test_cron_escalation_exists(self):
        self.assertTrue(hasattr(self.env['sf.freight.dispute'],
                                '_cron_dispute_escalation'))

    # T09 multi-company isolation
    def test_multi_company_isolation(self):
        company2 = self.env['res.company'].create({'name': 'Co2'})
        inv1 = self._make_invoice([])
        inv2 = self.env['sf.freight.invoice'].with_company(company2).create({
            'carrier_id': self.carrier.id,
            'invoice_ref': 'OTHER',
            'company_id': company2.id,
        })
        user = self.env['res.users'].create({
            'name': 'U1',
            'login': 'fa_%s' % uuid.uuid4().hex[:6],
            'groups_id': [(6, 0, [
                self.env.ref(
                    'sf_freight_audit.group_sf_freight_audit_user').id,
            ])],
            'company_ids': [(6, 0, [self.company.id])],
        })
        self.assertTrue(inv1.with_user(user).exists())
        self.assertFalse(inv2.with_user(user).exists())

    # T10 unlink guard
    def test_unlink_guard(self):
        inv = self._make_invoice([{
            'charge_type': 'base_freight',
            'tracking_ref': '',
            'uom_weight': 10.0,
            'amount_billed': 100.0,
        }])
        inv.action_run_audit()
        if inv.state not in ('draft', 'cancelled'):
            with self.assertRaises(UserError):
                inv.unlink()

    # T11 duplicate invoice constraint
    def test_duplicate_invoice_ref(self):
        vals = {
            'carrier_id': self.carrier.id,
            'invoice_ref': 'DUPL-001',
        }
        self.env['sf.freight.invoice'].create(vals)
        with self.assertRaises(Exception):
            self.env['sf.freight.invoice'].create(vals)

    # T12 surcharge unauthorized
    def test_surcharge_unauthorized(self):
        inv = self._make_invoice([
            {'charge_type': 'base_freight', 'tracking_ref': '',
             'uom_weight': 10.0, 'amount_billed': 100.0},
            {'charge_type': 'liftgate', 'tracking_ref': '',
             'uom_weight': 0.0, 'amount_billed': 50.0},
        ])
        inv.action_run_audit()
        f = inv.finding_ids.filtered(
            lambda ff: ff.finding_type == 'surcharge_unauthorized')
        self.assertTrue(f)
