{
    'name': 'Certificate of Analysis (CoA) Generator',
    'version': '18.0.1.0.0',
    'category': 'Quality/Quality',
    'summary': 'Generate certificates of analysis per delivery: test parameters, specifications, results and approval workflow',
    'description': """
Certificate of Analysis Generator
=================================

Ship with proof of quality, every time.

Features:
---------
* CoA records per delivery picking: lines from picking moves with lots
* Test parameters: specification, measured result, pass/fail verdict
* Approval workflow: draft, tested, approved, issued
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'stock', 'quality', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/coa_security.xml',
        'data/coa_data.xml',
        'views/coa_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
