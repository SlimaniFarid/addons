{
    'name': 'Currency Exposure Heatmap',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Net open FX position per currency pair with hedging recommendation.',
    'description': """
Currency Exposure Heatmap
=========================

Net open FX position per currency pair with hedging recommendation.

Features:
---------
* Workflow with status tracking
* Chatter and activities
* Multi-company isolation
* Configurable sequences
* Role-based security groups

Standard Odoo modules only. Multi-company ready. Full audit trail.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.25,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
