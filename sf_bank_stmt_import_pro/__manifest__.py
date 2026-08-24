{
    'name': 'Bank Statement Import Pro (MT940 / CAMT / CSV)',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Import any bank statement: MT940, CAMT.053, OFX, QIF or any bank CSV - per-bank templates, duplicate detection, multi-currency',
    'description': """
Bank Statement Import Pro
=========================

Import any bank statement file into Odoo Accounting, ready for
reconciliation. No bank feed required.

Supported Formats:
------------------
* MT940 (SWIFT / German banks)
* CAMT.053 (ISO 20022 SEPA statements)
* OFX and QIF (US / international banks)
* Any bank CSV via saved per-bank templates

Key Features:
-------------
* Per-bank import templates: column mapping, delimiters, date format,
  decimal/thousand separators, encoding - saved once, reused forever
* Guided flow: upload file -> parse preview -> review -> import
* Duplicate detection: hash of date + amount + reference compared
  against existing statement lines and current batch; duplicates
  flagged and skipped (force-import option)
* Opening/closing balances read from MT940 and CAMT.053
* Multi-currency: foreign-currency lines keep amount_currency and
  currency when the rate exists in Odoo
* Partner resolution by exact name match; unmatched lines stay
  unreconciled-ready
* Import history with stats: total, imported, duplicates, errors
* Multi-company safe via journal company

Workflow:
---------
1. Accounting -> Bank Import Pro -> Templates: create one template
   per bank/file layout (or use MT940/CAMT/OFX/QIF directly)
2. Bank Import Pro -> Import Runs: New, pick journal + template,
   upload the file, click Parse File
3. Review the preview: duplicates flagged, errors shown per line
4. Click Import Lines: statement + lines created, ready to reconcile

No third-party Python libraries required - pure Odoo + stdlib.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 299.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/bank_security.xml',
        'data/bank_data.xml',
        'views/bank_views.xml',
    ],
    'demo': [
        'data/bank_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
