{
    'name': 'Retail Store Credit & Customer Wallet',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Customer store credit accounts, reusable credit grants, usage, adjustments, expirations and balances',
    'description': """
Store Credit
============

Customer store credit accounts, reusable credit grants, usage, adjustments, expirations and balances

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
    'depends': ['base', 'mail', 'contacts', 'sale'],
    'data': ['security/sf_store_credit_security.xml', 'security/ir.model.access.csv', 'data/sf_store_credit_sequence.xml', 'data/sf_store_credit_cron.xml', 'data/sf_store_credit_report.xml', 'views/sf_store_credit_account_views.xml', 'views/sf_store_credit_credit_views.xml', 'views/sf_store_credit_adjust_wizard_views.xml', 'views/sf_store_credit_menus.xml', 'views/report_store_credit_account.xml', 'views/report_store_credit.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}
