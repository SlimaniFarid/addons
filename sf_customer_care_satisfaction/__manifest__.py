{
    'name': 'Post-Interaction Satisfaction',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Capture satisfaction after each customer interaction: rating, comments and follow-up.',
    'description': """
Post-Interaction Satisfaction
=============================

Capture satisfaction after each customer interaction: rating, comments and follow-up.

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
    'price': 44.75,
    'currency': 'EUR',
    'depends': ['base', 'sale', 'mail'],
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
