{
    'name': 'B2B Price & Discount Matrix',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Tiered pricing and discount matrix per customer category',
    'description': """
Price Matrix
============

Tiered pricing and discount matrix per customer category

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
    'depends': ['base', 'sale', 'product', 'account'],
    'data': ['security/price_matrix_security.xml', 'security/ir.model.access.csv', 'data/price_matrix_data.xml', 'views/price_matrix_menus.xml', 'views/price_matrix_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
