{
    'name': 'Employee 1-on-1 Tracker',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Track regular 1-on-1 meetings: topics, feedback, development actions and mood.',
    'description': """
Employee 1-on-1 Tracker
=======================

Track regular 1-on-1 meetings: topics, feedback, development actions and mood.

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
    'price': 49.75,
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
