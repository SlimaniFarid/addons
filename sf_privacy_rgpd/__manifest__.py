{
    'name': 'Privacy & RGPD',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Data protection register (RGPD): treatments, processors, DPIA, breach and data subject rights management',
    'description': """
Privacy Rgpd
============

Data protection register (RGPD): treatments, processors, DPIA, breach and data subject rights management

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
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/privacy_security.xml', 'security/ir.model.access.csv', 'views/privacy_views.xml', 'views/res_config_settings_views.xml', 'views/privacy_reports.xml', 'views/privacy_menus.xml', 'data/privacy_data.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
