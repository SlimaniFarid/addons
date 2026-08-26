{
    'name': 'Supplier Scorecard Review Meetings',
    'version': '19.0.1.0.0',
    'category': 'Purchase/Purchase',
    'summary': 'Quarterly supplier review meetings: scores, action plans and improvement commitments.',
    'description': """
Supplier Scorecard Review Meetings
==================================

Quarterly supplier review meetings: scores, action plans and improvement commitments.

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
    'depends': ['base', 'purchase', 'mail'],
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
