{
    'name': 'Cold Chain Monitoring',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Monitor temperature excursions on cold storage sites and transport trips with alerts and reports',
    'description': """
Cold Chain
==========

Monitor temperature excursions on cold storage sites and transport trips with alerts and reports

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
    'depends': ['base', 'mail'],
    'data': ['security/sf_cold_chain_security.xml', 'security/ir.model.access.csv', 'data/sf_cold_chain_sequence.xml', 'data/sf_cold_chain_cron.xml', 'data/sf_cold_chain_report.xml', 'views/sf_cold_site_views.xml', 'views/sf_cold_trip_views.xml', 'views/sf_cold_reading_views.xml', 'views/sf_cold_excursion_views.xml', 'views/sf_cold_chain_menus.xml', 'views/report_cold_log.xml', 'views/res_config_settings_views.xml', 'views/sf_cold_chain_report_wizard_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
