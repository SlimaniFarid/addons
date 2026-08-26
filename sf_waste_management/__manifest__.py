{
    'name': 'Waste Management (BSD)',
    'version': '18.0.1.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Waste tracking slips (BSD), sites and waste codes',
    'description': """
Waste Management
================

Waste tracking slips (BSD), sites and waste codes

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
    'website': 'https://tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts', 'web'],
    'data': ['security/waste_groups.xml', 'security/ir.model.access.csv', 'data/waste_data.xml', 'views/waste_views.xml', 'views/waste_reports.xml', 'views/waste_menus.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
