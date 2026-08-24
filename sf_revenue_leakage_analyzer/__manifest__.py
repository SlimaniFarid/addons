{
    'name': 'Revenue Leakage Analyzer',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Detect revenue leakage: unbilled services, expired discounts, missed escalations.',
    'description': """
Revenue Leakage Analyzer
========================

Detect revenue leakage: unbilled services, expired discounts, missed escalations.

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
    'price': 69.75,
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
