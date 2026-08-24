{
    'name': 'Daily Production Meeting Actions',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/MES',
    'summary': 'Daily production meeting: attendance, topics, action items with owners and due dates.',
    'description': """
Daily Production Meeting Actions
================================

Daily production meeting: attendance, topics, action items with owners and due dates.

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
    'depends': ['base', 'mrp', 'mail'],
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
