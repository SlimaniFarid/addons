{
    'name': 'Product End-of-Life & Last-Time-Buy',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Phase-out planning: EOL announcements, last-time-buy dates, replacement mapping, open order checks and sale blocking',
    'description': """
Product Eol
===========

Phase-out planning: EOL announcements, last-time-buy dates, replacement mapping, open order checks and sale blocking

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
    'depends': ['base', 'product', 'sale', 'stock', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/eol_security.xml', 'data/eol_data.xml', 'views/eol_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
