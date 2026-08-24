{
    'name': 'Intercompany Reconciliation & Netting',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Match open intercompany balances across entities, compute net positions per company pair and generate settlement entries',
    'description': """
Intercompany Reconciliation and Netting
=======================================

Close the month without the intercompany spreadsheet marathon.

Features:
---------
* Netting sessions per period across selected entities
* Automatic scan of posted receivable/payable journal items whose
  partner is another group company (matched via company partner record)
* Net position per company pair: receivables minus payables, with
  invoice counts and unmatched item drill-down
* Dispute tracking on individual items with resolution notes
* Settlement entries generated for net amounts (due to / due from)
* Multi-currency, multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 299.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/ic_security.xml',
        'data/ic_data.xml',
        'views/ic_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
