{
    'name': 'Production Trial Tracking',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/MES',
    'summary': 'Track trial runs before series production: parameters, results and go/no-go decisions.',
    'description': """
Production Trial Tracking
=========================

Track trial runs before series production: parameters, results and go/no-go decisions.

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
    'depends': ['base', 'mrp', 'mail'],
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
