{
    'name': 'Credit Insurance & Insured Exposure',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Insurer policies, approved buyer limits with coverage %, and bad-debt claims with indemnity tracking',
    'description': """
Credit Insurance Management
===========================

Insure your receivables, track your coverage, recover your losses.

Features:
---------
* Insurance policies: insurer, policy number, coverage %, premium,
  period
* Insured buyer requests: requested vs approved limit, coverage %,
  insurer decision workflow
* Claims on overdue/bad debt: filed amount, indemnity computed from
  coverage, settlement states (submitted, accepted, paid, rejected)
* Multi-company, currencies, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/ci_security.xml',
        'data/ci_data.xml',
        'views/ci_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
