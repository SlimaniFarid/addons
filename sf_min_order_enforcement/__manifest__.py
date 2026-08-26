{
    'name': 'Minimum Order Enforcement',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Minimum order value and quantity rules per customer segment with override approval.',
    'description': """
Minimum Order Enforcement
=========================

Minimum order value and quantity rules per customer segment with override approval.

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
