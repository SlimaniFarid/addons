{
    'name': 'EHS Inspection Scheduler',
    'version': '19.0.1.0.0',
    'category': 'HR/Health & Safety',
    'summary': 'Schedule EHS inspections per site/area with checklists, findings and corrective links.',
    'description': """
EHS Inspection Scheduler
========================

Schedule EHS inspections per site/area with checklists, findings and corrective links.

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
    'depends': ['base', 'hr', 'mail'],
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
