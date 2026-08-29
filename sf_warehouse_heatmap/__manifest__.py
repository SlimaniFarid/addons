{
    'name': 'Warehouse Activity Heatmap',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Activity heatmap for slotting optimization: pick frequency, travel distance and ABC classification.',
    'description': """
Warehouse Heatmap
=================

Activity heatmap for slotting optimization: pick frequency, travel distance and ABC classification.

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
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': ['security/sf_warehouse_heatmap_security.xml', 'security/ir.model.access.csv', 'data/sf_warehouse_heatmap_sequence.xml', 'views/slotting_analysis_views.xml', 'views/slotting_result_views.xml', 'views/sf_warehouse_heatmap_menus.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
