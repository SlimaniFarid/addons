{
    'name': 'First Article Inspection (FAI)',
    'version': '18.0.1.0',
    'category': 'Quality/Quality',
    'summary': 'First Article Inspection per AS9102/AS9145 for aerospace/automotive',
    'description': """
First Article Inspection
========================

First Article Inspection per AS9102/AS9145 for aerospace/automotive

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
    'depends': ['base', 'quality', 'mrp', 'stock', 'mail'],
    'data': ['security/fai_security.xml', 'security/ir.model.access.csv', 'data/fai_data.xml', 'views/fai_menus.xml', 'views/fai_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
