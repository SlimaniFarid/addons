{
    'name': 'Scrap Reason Analytics',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/MES',
    'summary': 'Coded scrap with reason tree, Pareto analysis and improvement action tracking.',
    'description': """
Scrap Reason Analytics
======================

Coded scrap with reason tree, Pareto analysis and improvement action tracking.

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
    'depends': ['base', 'mrp', 'mail', 'stock'],
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
