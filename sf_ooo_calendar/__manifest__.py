{
    'name': 'Out-of-Office & Backup Calendar',
    'version': '18.0.1.0.0',
    'category': 'IT/Operations',
    'summary': 'OOO periods with backup assignment and handover notes, visible to teams.',
    'description': """
Out-of-Office & Backup Calendar
===============================

OOO periods with backup assignment and handover notes, visible to teams.

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
    'price': 37.25,
    'currency': 'EUR',
    'depends': ['base', 'hr', 'mail'],
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
