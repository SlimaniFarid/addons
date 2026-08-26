{
    'name': 'Customer Feedback Action Tracker',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Convert customer feedback into tracked actions with owners, due dates and closure validation.',
    'description': """
Customer Feedback Action Tracker
================================

Convert customer feedback into tracked actions with owners, due dates and closure validation.

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
