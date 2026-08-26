{
    'name': 'Direct Print PRO',
    'version': '18.0.1.0',
    'category': 'Productivity',
    'summary': 'Print reports & labels directly to network/Bluetooth printers',
    'description': """
Direct Print Pro
================

Print reports & labels directly to network/Bluetooth printers

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
    'depends': ['base', 'stock', 'sale', 'account', 'mail'],
    'data': ['security/ir.model.access.csv', 'views/print_menus.xml', 'data/print_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
