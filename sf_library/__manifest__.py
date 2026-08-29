{
    'name': 'Library & Media Center Management',
    'version': '18.0.1.0',
    'category': 'Other/Others',
    'summary': 'Catalogue, members, loans, returns, late fees and reservations with cron alerts',
    'description': """
Library
=======

Catalogue, members, loans, returns, late fees and reservations with cron alerts

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
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/sf_library_security.xml', 'security/ir.model.access.csv', 'views/sf_library_views.xml', 'views/sf_library_reports.xml', 'views/res_config_settings_views.xml', 'views/sf_library_menus.xml', 'data/actions.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
