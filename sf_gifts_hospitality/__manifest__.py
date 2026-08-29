{
    'name': 'Corporate Gifts & Hospitality Register',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Anti-bribery register of gifts and hospitality given or received with approval threshold',
    'description': """
Gifts Hospitality
=================

Anti-bribery register of gifts and hospitality given or received with approval threshold

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
    'data': ['security/sf_gifts_hospitality_security.xml', 'security/ir.model.access.csv', 'data/sf_gifts_hospitality_sequence.xml', 'data/sf_gifts_hospitality_report.xml', 'views/sf_gifts_hospitality_views.xml', 'views/sf_gifts_hospitality_menus.xml', 'views/report_gift_register.xml', 'views/report_gift_declaration.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
