{
    'name': 'Packaging Consigns Management',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Returnable packaging consigns: deposit types, parks per site, emissions/returns linked to deliveries, invoiced deposits, return rate and stock alerts',
    'description': """
Packaging Consigns
==================

Returnable packaging consigns: deposit types, parks per site, emissions/returns linked to deliveries, invoiced deposits, return rate and stock alerts

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
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/packaging_security.xml', 'security/ir.model.access.csv', 'views/packaging_views.xml', 'views/res_config_settings_views.xml', 'views/packaging_reports.xml', 'views/packaging_menus.xml', 'data/packaging_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
