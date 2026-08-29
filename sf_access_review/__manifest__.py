{
    'name': 'Access Recertification Campaigns',
    'version': '18.0.1.0.0',
    'category': 'Administration/Administrators',
    'summary': 'Periodic user access reviews: campaign per scope, per-user group review with keep/revoke decisions and evidence',
    'description': """
Access Review
=============

Periodic user access reviews: campaign per scope, per-user group review with keep/revoke decisions and evidence

**Why you need this**

Stop losing time on spreadsheets and manual tracking.
This module gives your team a dedicated tool inside Odoo,
fully integrated with your existing data.

**Key features**

* One-click workflow from draft to done
* Kanban view for instant visual overview
* Smart filters (My records, To-do) save time daily
* Overdue detection highlights urgent items automatically
* Responsible user assignment with full tracking

**Getting started**

Install and start creating records immediately.
No configuration needed.

""",
    'author': 'Ethan Miller',
    'license': 'OPL-1',
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/ar_security.xml', 'data/ar_data.xml', 'views/ar_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
