{
    'name': 'Prepaid Expense Amortization',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Track prepaid expenses (insurance, subscriptions, rent) with monthly amortization schedules.',
    'description': """
Prepaid Expense Amortization
============================

Track prepaid expenses (insurance, subscriptions, rent) with monthly amortization schedules.

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
    'price': 57.25,
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
