{
    'name': 'IT Asset & License Manager',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Track IT equipment, software licenses, assignments and warranties',
    'description': """
It Asset Management
===================

Track IT equipment, software licenses, assignments and warranties

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
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'hr'],
    'data': ['data/it_asset_data.xml', 'data/it_asset_cron.xml', 'security/it_asset_security.xml', 'security/ir.model.access.csv', 'views/it_asset_menus.xml', 'views/it_asset_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
