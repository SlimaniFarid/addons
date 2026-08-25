{
    'name': 'Software License Renewal Register',
    'version': '19.0.1.0.0',
    'category': 'IT/Operations',
    'summary': 'License subscriptions with renewal dates, costs, seats and auto-renewal risk flags.',
    'description': """
Software License Renewal Register
=================================

License subscriptions with renewal dates, costs, seats and auto-renewal risk flags.

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
    'depends': ['base', 'mail'],
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
