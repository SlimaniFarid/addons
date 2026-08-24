{
    'name': 'Min/Max Parameter Review',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Periodic review workflow for min/max stock parameters with demand evidence and approval.',
    'description': """
Min/Max Parameter Review
========================

Periodic review workflow for min/max stock parameters with demand evidence and approval.

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
