{
    'name': 'Customer Revenue Trend Alerts',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Detect customers with revenue drops beyond thresholds for proactive action.',
    'description': """
Customer Revenue Trend Alerts
=============================

Detect customers with revenue drops beyond thresholds for proactive action.

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
    'depends': ['base', 'account', 'sale', 'mail'],
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
