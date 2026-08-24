{
    'name': 'FX Exposure & Hedging Manager',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Open FX exposure per currency from receivables/payables, forward contracts with settlement gain/loss tracking',
    'description': """
FX Exposure and Hedging Manager
===============================

Know your currency risk and prove what your hedges did.

Features:
---------
* Exposure snapshots: net open position per currency computed from
  posted foreign-currency receivables and payables
* Forward contracts: direction (buy/sell), notional, strike rate,
  value date, counterparty bank
* At maturity: settlement with spot rate, realized gain/loss computed
  and tracked
* Hedge coverage ratio per currency: hedged vs open exposure
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 74.75,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/fx_security.xml',
        'data/fx_data.xml',
        'views/fx_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
