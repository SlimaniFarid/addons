{
    'name': 'BOM Change Requests',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/MES',
    'summary': 'Request and approve BOM changes: component swaps, qty changes with effectivity dates and cost impact.',
    'description': """
BOM Change Requests
===================

Request and approve BOM changes: component swaps, qty changes with effectivity dates and cost impact.

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
    'images': ['static/description/banner.png'],
}
