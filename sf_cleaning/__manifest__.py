{
    'name': 'Cleaning Services & Contracts',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Cleaning service contracts, schedules, interventions, quality checks and invoicing',
    'description': """
Cleaning
========

Cleaning service contracts, schedules, interventions, quality checks and invoicing

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
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/sf_cleaning_security.xml', 'security/ir.model.access.csv', 'views/sf_cleaning_views.xml', 'views/sf_cleaning_reports.xml', 'views/res_config_settings_views.xml', 'views/sf_cleaning_menus.xml', 'data/actions.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
