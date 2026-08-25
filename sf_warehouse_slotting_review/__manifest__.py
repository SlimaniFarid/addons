{
    'name': 'Warehouse Slotting Review',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Review product slotting: velocity, weight, size vs current location with move recommendations.',
    'description': """
Warehouse Slotting Review
=========================

Review product slotting: velocity, weight, size vs current location with move recommendations.

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
