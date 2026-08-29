{
    'name': 'Production Master Scheduling (MPS)',
    'version': '18.0.1.0',
    'category': 'Manufacturing',
    'summary': 'Master production schedule with Gantt, priorities and work center load',
    'description': """
Production Planning
===================

Master production schedule with Gantt, priorities and work center load

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
    'depends': ['base', 'mail', 'mrp'],
    'data': ['security/production_security.xml', 'security/ir.model.access.csv', 'views/production_views.xml', 'views/production_reports.xml', 'views/res_config_settings_views.xml', 'views/production_menus.xml', 'data/production_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
