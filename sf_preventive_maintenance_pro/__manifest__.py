{
    'name': 'Preventive Maintenance Pro',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'PM scheduling by meter reading or time triggers, work order auto-generation and compliance calendar.',
    'description': """
Preventive Maintenance Pro
==========================

PM scheduling by meter reading or time triggers, work order auto-generation and compliance calendar.

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
    'data': ['security/sf_preventive_maintenance_pro_security.xml', 'security/ir.model.access.csv', 'data/sf_preventive_maintenance_pro_sequence.xml', 'views/pm_plan_views.xml', 'views/pm_work_order_views.xml', 'views/sf_preventive_maintenance_pro_menus.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
