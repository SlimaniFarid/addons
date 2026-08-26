{
    'name': 'Quality Alert Aging Monitor',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Monitor open quality alerts by age with escalation at thresholds.',
    'description': """
Quality Alert Aging Monitor
===========================

Monitor open quality alerts by age with escalation at thresholds.

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
    'depends': ['base', 'quality', 'mail'],
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
