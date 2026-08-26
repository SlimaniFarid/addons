{
    'name': 'Team Capacity Planner',
    'version': '18.0.1.0.0',
    'category': 'IT/Operations',
    'summary': 'Plan team capacity: members, availability, allocation and over-allocation alerts.',
    'description': """
Team Capacity Planner
=====================

Plan team capacity: members, availability, allocation and over-allocation alerts.

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
