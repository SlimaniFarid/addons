{
    'name': 'Utility & Sub-Meter Billing',
    'version': '18.0.1.0',
    'category': 'Accounting',
    'summary': 'Delivery points and meters registry, reading campaigns, tiered tariffs and consumption invoices',
    'description': """
Utility Billing
===============

Delivery points and meters registry, reading campaigns, tiered tariffs and consumption invoices

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
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'uom', 'contacts', 'account'],
    'data': ['security/sf_utility_security.xml', 'security/ir.model.access.csv', 'data/sf_utility_sequence.xml', 'data/sf_utility_cron.xml', 'data/sf_utility_report.xml', 'views/sf_utility_meter_views.xml', 'views/sf_utility_reading_views.xml', 'views/sf_utility_import_wizard_views.xml', 'views/sf_utility_campaign_views.xml', 'views/sf_utility_tariff_views.xml', 'views/sf_utility_invoice_views.xml', 'views/sf_utility_menus.xml', 'views/report_reading.xml', 'views/report_campaign.xml', 'views/report_invoice.xml', 'views/report_overdue.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
