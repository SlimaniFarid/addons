{
    'name': 'Replenishment Review Queue',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Review queue for reorder proposals: demand check, approval and order emission tracking.',
    'description': """
Replenishment Review Queue
==========================

Review queue for reorder proposals: demand check, approval and order emission tracking.

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
    'depends': ['base', 'stock', 'purchase', 'mail'],
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
