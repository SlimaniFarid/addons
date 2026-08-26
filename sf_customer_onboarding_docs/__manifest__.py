{
    'name': 'Customer Document Collection',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Request and track document collection from customers (specs, drawings, compliance forms).',
    'description': """
Customer Document Collection
============================

Request and track document collection from customers (specs, drawings, compliance forms).

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
    'price': 37.25,
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
