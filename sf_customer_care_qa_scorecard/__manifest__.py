{
    'name': 'Care QA Scorecard',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'QA scorecards for customer care: interaction review, scoring and coaching links.',
    'description': """
Care QA Scorecard
=================

QA scorecards for customer care: interaction review, scoring and coaching links.

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
