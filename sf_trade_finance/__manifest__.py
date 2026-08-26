{
    'name': 'Trade Finance — LC & Bank Guarantees',
    'version': '18.0.1.0',
    'category': 'Finance',
    'summary': 'Letters of credit, bank guarantees and documentary collections with key dates and documents',
    'description': """
Trade Finance
=============

Letters of credit, bank guarantees and documentary collections with key dates and documents

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
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'sale', 'purchase', 'account', 'mail'],
    'data': ['security/trade_security.xml', 'security/ir.model.access.csv', 'views/trade_views.xml', 'views/res_config_settings_views.xml', 'views/trade_menus.xml', 'data/trade_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
