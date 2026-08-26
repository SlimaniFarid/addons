{
    'name': 'Warehouse Wave Picking',
    'version': '18.0.1.0',
    'category': 'Inventory/Inventory',
    'summary': 'Group pickings into waves and release them efficiently',
    'description': """
Wave Picking
============

Group pickings into waves and release them efficiently

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
    'depends': ['base', 'stock', 'stock_picking_batch', 'mail'],
    'data': ['security/wave_picking_security.xml', 'security/ir.model.access.csv', 'views/wave_picking_menus.xml', 'views/wave_picking_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
