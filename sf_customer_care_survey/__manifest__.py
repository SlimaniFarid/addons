{
    'name': 'Customer Care Survey Runner',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Run customer care surveys: NPS, CSAT, CES with response tracking and actions.',
    'description': """
Customer Care Survey Runner
===========================

Run customer care surveys: NPS, CSAT, CES with response tracking and actions.

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
    'images': ['static/description/banner.png'],
}
