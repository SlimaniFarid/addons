{
    'name': '8D Complaint Management',
    'version': '18.0.1.0.0',
    'category': 'Quality',
    'summary': '8D methodology: team formation, root cause, corrective actions, CAPA tracking and supplier notification.',
    'description': """
Complaint 8D
============

8D methodology: team formation, root cause, corrective actions, CAPA tracking and supplier notification.

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
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': ['security/sf_complaint_8d_security.xml', 'security/ir.model.access.csv', 'data/sf_complaint_8d_sequence.xml', 'views/complaint_8d_views.xml', 'views/sf_complaint_8d_menus.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
