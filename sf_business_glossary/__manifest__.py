{
    'name': 'Business Glossary & Data Dictionary',
    'version': '19.0.1.0.0',
    'category': 'IT/Operations',
    'summary': 'Shared business terms: definition, owner, source system and related KPIs.',
    'description': """
Business Glossary & Data Dictionary
===================================

Shared business terms: definition, owner, source system and related KPIs.

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
