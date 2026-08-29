{
    'name': 'Field Sales Routes & Territory Management',
    'version': '18.0.1.0',
    'category': 'Sales',
    'summary': 'Plan field sales routes, track visits, territories and objectives',
    'description': """
Sales Routes
============

Plan field sales routes, track visits, territories and objectives

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
    'depends': ['base', 'sale', 'crm'],
    'data': ['security/routes_security.xml', 'security/ir.model.access.csv', 'views/routes_menus.xml', 'views/routes_views.xml', 'data/routes_cron.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
