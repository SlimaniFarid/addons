{
    'name': 'Rework Management',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Track rework orders, operations and scrap with cost computation and escalation alerts',
    'description': """
Rework Management
=================

Track rework orders, operations and scrap with cost computation and escalation alerts

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
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'product', 'stock', 'contacts'],
    'data': ['security/sf_rework_management_security.xml', 'security/ir.model.access.csv', 'data/sf_rework_management_sequence.xml', 'data/sf_rework_management_cron.xml', 'data/sf_rework_management_report.xml', 'views/sf_rework_order_views.xml', 'views/sf_rework_management_menus.xml', 'views/report_rework_order.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}
