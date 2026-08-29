{
    'name': 'Shop Floor Data Terminal',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Shop floor terminal for work order tracking, time logging, quantity reporting and scrap entry.',
    'description': """
Shop Floor Terminal
===================

Shop floor terminal for work order tracking, time logging, quantity reporting and scrap entry.

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
    'data': ['security/sf_shop_floor_terminal_security.xml', 'security/ir.model.access.csv', 'data/sf_shop_floor_terminal_sequence.xml', 'views/shop_floor_entry_views.xml', 'views/sf_shop_floor_terminal_menus.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
