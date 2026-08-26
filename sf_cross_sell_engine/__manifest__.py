{
    'name': 'Cross-Sell Recommendation Engine',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Define product affinity rules for cross-sell recommendations at quote time.',
    'description': """
Cross-Sell Recommendation Engine
================================

Define product affinity rules for cross-sell recommendations at quote time.

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
}
