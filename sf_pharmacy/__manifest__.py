{
    'name': 'Pharmacy & Dispensation Management',
    'version': '18.0.1.0',
    'category': 'Sales',
    'summary': 'Pharmacy management: products, batches, expiries and prescription dispensations',
    'description': """
Pharmacy
========

Pharmacy management: products, batches, expiries and prescription dispensations

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
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/sf_pharmacy_security.xml', 'security/ir.model.access.csv', 'views/sf_pharmacy_views.xml', 'views/res_config_settings_views.xml', 'views/sf_pharmacy_reports.xml', 'data/actions.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
