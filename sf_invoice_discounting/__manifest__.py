{
    'name': 'Invoice Discounting & Factoring Register',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Register factored/discounted invoices: advance %, fees, maturity and repurchase tracking.',
    'description': """
Invoice Discounting & Factoring Register
========================================

Register factored/discounted invoices: advance %, fees, maturity and repurchase tracking.

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
    'price': 69.75,
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
    'images': ['static/description/banner.png'],
}
