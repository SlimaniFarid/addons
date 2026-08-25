{
    'name': 'Production Capacity Plan',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Capacity planning per workcenter: available hours, load, over/under capacity.',
    'description': """
Production Capacity Plan
========================

Capacity planning per workcenter: available hours, load, over/under capacity.

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
    'depends': ['base', 'sale', 'mail', 'mrp'],
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
