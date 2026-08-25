{
    'name': 'Policy Exception & Waiver Management',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Employees',
    'summary': 'Time-boxed policy waivers with risk assessment, compensating controls and approval workflow',
    'description': """
Policy Exception and Waiver Management
======================================

Exceptions with expiry dates, not open doors.

Features:
---------
* Waiver requests per policy: reason, risk assessment,
  compensating controls, validity window
* Approval workflow with approver and decision date
* Automatic expiry flag; renewal requires a new request
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 44.75,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/pw_security.xml',
        'data/pw_data.xml',
        'views/pw_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
