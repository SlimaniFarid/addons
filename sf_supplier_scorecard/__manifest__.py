{
    'name': 'Supplier Scorecard & Quality',
    'version': '19.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Score suppliers on delivery, quality and compliance',
    'description': """
Supplier Scorecard
==================

Score suppliers on delivery, quality and compliance

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
    'price': 29.95,
    'currency': 'EUR',
    'depends': ['base', 'purchase', 'stock', 'quality'],
    'data': ['security/supplier_scorecard_security.xml', 'security/ir.model.access.csv', 'views/supplier_scorecard_menus.xml', 'views/supplier_scorecard_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
