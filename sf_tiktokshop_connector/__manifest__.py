{
    'name': 'TikTok Shop Connector',
    'version': '18.0.1.0',
    'category': 'eCommerce',
    'summary': 'Sync products, orders and stock with TikTok Shop',
    'description': """
Tiktokshop Connector
====================

Sync products, orders and stock with TikTok Shop

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
    'depends': ['base', 'sale', 'stock', 'account'],
    'data': ['security/ir.model.access.csv', 'views/tiktokshop_menus.xml', 'views/tiktokshop_product_views.xml', 'views/tiktokshop_order_views.xml', 'views/tiktokshop_sync_log_views.xml', 'data/tiktokshop_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
