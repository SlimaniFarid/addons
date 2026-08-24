{
    'name': 'Access Recertification Campaigns',
    'version': '18.0.1.0.0',
    'category': 'Administration/Administrators',
    'summary': 'Periodic user access reviews: campaign per scope, per-user group review with keep/revoke decisions and evidence',
    'description': """
Access Recertification
======================

Prove that access rights stay legitimate.

Features:
---------
* Campaigns: scope (all users / admins only), due date
* Review lines auto-generated per user: groups summary, reviewer
  decision (keep / revoke), comments
* Evidence trail for auditors: campaign, decisions, dates
* Multi-company, chatter
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 57.25,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/ar_security.xml',
        'data/ar_data.xml',
        'views/ar_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
