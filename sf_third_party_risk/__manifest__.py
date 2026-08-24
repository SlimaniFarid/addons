{
    'name': 'Third-Party Risk Assessment',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Assess third-party risks: vendor, data access, criticality and mitigation plan.',
    'description': """
Third-Party Risk Assessment
===========================

Assess third-party risks: vendor, data access, criticality and mitigation plan.

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
