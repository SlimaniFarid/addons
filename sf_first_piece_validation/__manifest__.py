{
    'name': 'First-Piece Validation',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/MES',
    'summary': 'First-piece validation per setup: measurements, checklist and production release gate.',
    'description': """
First-Piece Validation
======================

First-piece validation per setup: measurements, checklist and production release gate.

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
    'depends': ['base', 'mrp', 'quality', 'mail'],
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
