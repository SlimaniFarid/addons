{
    'name': 'Reusable Checklist Library',
    'version': '18.0.1.0.0',
    'category': 'IT/Operations',
    'summary': 'Build reusable checklists (audits, onboarding, launches) and run instances with progress.',
    'description': """
Reusable Checklist Library
==========================

Build reusable checklists (audits, onboarding, launches) and run instances with progress.

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
    'depends': ['base', 'mail'],
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
