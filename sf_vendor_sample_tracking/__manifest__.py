{
    'name': 'Vendor Sample Request Tracking',
    'version': '18.0.1.0.0',
    'category': 'Purchase/Purchase',
    'summary': 'Request and track samples from suppliers: request, received, evaluated, approved for use.',
    'description': """
Vendor Sample Request Tracking
==============================

Request and track samples from suppliers: request, received, evaluated, approved for use.

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
    'depends': ['base', 'purchase', 'product', 'mail'],
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
