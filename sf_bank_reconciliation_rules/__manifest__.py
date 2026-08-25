{
    'name': 'Bank Reconciliation Rule Builder',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Build reusable bank statement reconciliation rules with priority, match percentages and auto-suggest application.',
    'description': """
Bank Reconciliation Rule Builder
================================

Build reusable bank statement reconciliation rules with priority, match percentages and auto-suggest application.

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
