{
    'name': 'PO Supplier Acknowledgment',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Track supplier PO acknowledgments: sent, confirmed, late and escalation.',
    'description': """
PO Supplier Acknowledgment
==========================

Track supplier PO acknowledgments: sent, confirmed, late and escalation.

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
