# -*- coding: utf-8 -*-
{
    'name': 'Freight Audit',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Audit carrier invoices against contracts and shipments: detect overcharges, manage disputes, recover money',
    'description': """
Freight Audit & Carrier Invoice Verification
============================================

Stop paying carrier billing errors silently. 5-10% of freight invoices
contain errors, almost always in the carrier's favor (Tompkins Ventures,
2026). This module audits every carrier invoice line against your
negotiated contracts and your real shipments.

Features:
- Carrier contracts with rate grids, tolerances and allowed surcharges
- CSV invoice import with dry-run validation and rejected-line report
- Automatic invoice-to-shipment matching (tracking ref + date + amount)
- Configurable verification rules: rate variance, unauthorized surcharge,
  weight/dim mismatch, duplicate billing, phantom shipment, VAT error
- Typed findings with severity levels and thresholds per contract
- Dispute workflow: submit, track carrier response, resolve by credit note
- Vendor credit note generation and automatic reconciliation
- Payment blocking while disputes are open
- Carrier compliance dashboard: conformity rate, recovered amounts
- Multi-company, multi-currency, full chatter audit trail

Recover the 3-10% of freight spend you are losing today.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'application': True,
    'installable': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': [
        'security/sf_freight_audit_security.xml',
        'security/ir.model.access.csv',
        'data/sf_freight_audit_sequence.xml',
        'data/sf_freight_audit_cron.xml',
        'views/sf_freight_contract_views.xml',
        'views/sf_freight_invoice_views.xml',
        'views/sf_freight_rule_views.xml',
        'views/sf_freight_audit_menus.xml',
        'report/sf_freight_audit_reports.xml',
    ],
}
