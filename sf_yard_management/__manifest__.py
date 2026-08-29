{
    'name': 'Yard Management',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Yard management: trailer inventory with dwell clocks, gate check-in/out, dock assignment, jockey shunts, detention billing',
    'description': """
Yard Management
===============

Yard management: trailer inventory with dwell clocks, gate check-in/out, dock assignment, jockey shunts, detention billing

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
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': ['security/sf_yard_management_security.xml', 'security/ir.model.access.csv', 'data/sf_yard_sequence.xml', 'models/res_partner.py', 'views/sf_yard_views.xml', 'views/sf_yard_menus.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
