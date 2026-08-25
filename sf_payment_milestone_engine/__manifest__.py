{
    'name': 'Payment Milestone Engine',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Define milestone-based payment terms on sales orders: percentages per milestone with due dates and tracking.',
    'description': """
Payment Milestone Engine
========================

Define milestone-based payment terms on sales orders: percentages per milestone with due dates and tracking.

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
    'depends': ['base', 'sale', 'account', 'mail'],
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
