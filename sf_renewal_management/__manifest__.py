{
    'name': 'Customer Contract Renewals & Notice Deadlines',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Renewal pipeline for customer contracts: notice deadlines, auto-renew flags, churn risk and renewal outcomes',
    'description': """
Customer Contract Renewals
==========================

Never miss a renewal deadline or lose a contract by silence.

Features:
---------
* Customer contracts: type, term, auto-renew, notice period,
  annual value, owner
* Notice deadline and expiry countdown computed automatically
* Churn risk rating and next action follow-up
* Renewal outcomes: renewed (with new end date), lost, expired
* Kanban pipeline by state, pivot by owner and type
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/renewal_security.xml',
        'data/renewal_data.xml',
        'views/renewal_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
