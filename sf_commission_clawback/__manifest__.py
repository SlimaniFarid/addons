{
    'name': 'Sales Commission Clawback',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Claw back commissions on returned or unpaid orders: rules, cases and recovery tracking.',
    'description': """
Sales Commission Clawback
=========================

Claw back commissions on returned or unpaid orders: rules, cases and recovery tracking.

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
}
