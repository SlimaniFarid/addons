{
    'name': 'Transfer Pricing Engine & OECD Documentation',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Intercompany arm-length pricing policies (CUP, cost-plus, resale-minus, TNMM), variance analysis and Master File / Local File documentation',
    'description': """
Transfer Pricing Engine
=======================

Apply OECD-compliant transfer pricing methods to intercompany transactions
and produce the documentation tax authorities expect.

Features:
---------
* Pricing policies per company pair: CUP, Cost-Plus, Resale-Minus,
  TNMM with markup % or target margin, validity dates, APA reference
* Scan posted intercompany invoices and compute the arm's length
  price under the applicable policy; variance and variance % flagged
* Threshold-based review workflow: transactions beyond tolerance
  require documented review
* Documentation register: Master File and Local File per fiscal year
  with sections, owner, review date and status
* Multi-company, currencies, full chatter audit trail

Compliance references: OECD TPG 2022 chapters I-II, BEPS Action 13
(Master File / Local File / CbCR ready).
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 99.75,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/tp_security.xml',
        'data/tp_data.xml',
        'views/tp_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
