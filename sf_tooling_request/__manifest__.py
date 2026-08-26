{
    'name': 'Tooling Request & Preparation',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/MES',
    'summary': 'Request tooling preparation per production order: tools needed, readiness status and delays.',
    'description': """
Tooling Request & Preparation
=============================

Request tooling preparation per production order: tools needed, readiness status and delays.

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
    'depends': ['base', 'mrp', 'mail'],
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
