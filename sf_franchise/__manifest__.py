{
    'name': 'Retail Franchise Network Management',
    'version': '18.0.1.0',
    'category': 'Sales',
    'summary': 'Franchise contracts, declared sales, automatic royalty calculation, invoicing and payment tracking',
    'description': """
Franchise
=========

Franchise contracts, declared sales, automatic royalty calculation, invoicing and payment tracking

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
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_franchise_security.xml', 'security/ir.model.access.csv', 'data/sf_franchise_sequence.xml', 'data/sf_franchise_cron.xml', 'data/sf_franchise_report.xml', 'views/sf_franchise_contract_views.xml', 'views/sf_franchise_declaration_views.xml', 'views/sf_franchise_menus.xml', 'views/report_franchise_contract.xml', 'views/report_franchise_declaration.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
