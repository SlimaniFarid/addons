{
    'name': 'Warehouse Zone Capacity Monitor',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Monitor occupancy per warehouse zone with max capacity alerts and relocation suggestions.',
    'description': """
Warehouse Zone Capacity Monitor
===============================

Monitor occupancy per warehouse zone with max capacity alerts and relocation suggestions.

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
    'depends': ['base', 'stock', 'mail'],
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
