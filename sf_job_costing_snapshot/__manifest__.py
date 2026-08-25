{
    'name': 'Job Costing Snapshot',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Project/job cost snapshots: labor, materials, overheads vs budget with margin alerts.',
    'description': """
Job Costing Snapshot
====================

Project/job cost snapshots: labor, materials, overheads vs budget with margin alerts.

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
    'images': ['static/description/banner.png'],
}
