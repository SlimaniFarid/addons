{
    'name': 'Remote Work Request Workflow',
    'version': '18.0.1.0.0',
    'category': 'Human Resources/Employees',
    'summary': 'Remote/telework requests with manager approval, days quota and equipment checklist.',
    'description': """
Remote Work Request Workflow
============================

Remote/telework requests with manager approval, days quota and equipment checklist.

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
}
