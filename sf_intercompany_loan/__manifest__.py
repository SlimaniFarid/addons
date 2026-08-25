{
    'name': 'Intercompany Loan Register',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'IC loans: principal, rate, schedule, interest postings and repayment tracking.',
    'description': """
Intercompany Loan Register
==========================

IC loans: principal, rate, schedule, interest postings and repayment tracking.

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
    'price': 74.75,
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
