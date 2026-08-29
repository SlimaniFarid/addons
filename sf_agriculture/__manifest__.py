{
    'name': 'Agriculture Management & Farm Operations',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Farms, plots, campaigns, cultures, treatments, harvests and inputs register for agriculture',
    'description': """
Agriculture
===========

Farms, plots, campaigns, cultures, treatments, harvests and inputs register for agriculture

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
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/agri_security.xml', 'security/ir.model.access.csv', 'views/agri_views.xml', 'views/agri_reports.xml', 'views/res_config_settings_views.xml', 'views/agri_menus.xml', 'data/agri_data.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
