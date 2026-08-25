{
    'name': 'Distributor Sell-Through Reporting',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Collect monthly sell-through and stock levels from distributors, compute weeks of channel stock.',
    'description': """
Distributor Sell-Through Reporting
==================================

Collect monthly sell-through and stock levels from distributors, compute weeks of channel stock.

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
    'depends': ['base', 'sale', 'product', 'mail'],
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
