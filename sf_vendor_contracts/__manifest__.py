{
    'name': 'Supplier Contract & Agreement Manager',
    'version': '18.0.1.0',
    'category': 'Purchases',
    'summary': 'Manage supplier contracts, clauses, amounts, expirations and renewals with alerts',
    'description': """
Vendor Contracts
================

Manage supplier contracts, clauses, amounts, expirations and renewals with alerts

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
    'depends': ['base', 'product', 'mail'],
    'data': ['data/vendor_contract_data.xml', 'data/vendor_contract_cron.xml', 'security/vendor_contract_security.xml', 'security/ir.model.access.csv', 'views/vendor_contract_menus.xml', 'views/vendor_contract_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
