{
    'name': 'Freight & Carrier Costing',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Track carriers, cost formulas and freight on pickings',
    'description': """
Freight Costing
===============

Track carriers, cost formulas and freight on pickings

**Why you need this**

Stop losing time on spreadsheets and manual tracking.
This module gives your team a dedicated tool inside Odoo,
fully integrated with your existing data.

**Key features**

* One-click workflow from draft to done
* Kanban view for instant visual overview
* Smart filters (My records, To-do) to save time daily
* Overdue detection highlights urgent items automatically
* Responsible user assignment with full tracking

**Getting started**

Install and start creating records immediately.
No configuration needed.

""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'stock', 'account'],
    'data': ['security/freight_costing_security.xml', 'security/ir.model.access.csv', 'views/freight_costing_menus.xml', 'views/freight_costing_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
