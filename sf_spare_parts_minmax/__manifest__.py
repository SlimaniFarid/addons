{
    'name': 'Spare Parts Min/Max',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Maintenance',
    'summary': 'Critical spare parts min/max with supplier lead times and stockout risk alerts.',
    'description': """
Spare Parts Min/Max
===================

Critical spare parts min/max with supplier lead times and stockout risk alerts.

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
    'depends': ['base', 'stock', 'product', 'mail'],
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
