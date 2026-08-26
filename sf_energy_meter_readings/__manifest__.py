{
    'name': 'Energy Meter Readings & Alerts',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Monthly meter readings per site with consumption trends and anomaly alerts.',
    'description': """
Energy Meter Readings & Alerts
==============================

Monthly meter readings per site with consumption trends and anomaly alerts.

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
    'price': 49.75,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
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
