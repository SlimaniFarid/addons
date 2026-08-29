{
    'name': 'Litigation & Legal Case Management',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Legal cases and pre-litigation: cases and parties, domains, procedural deadlines with alerts, fees and honoraries, decisions and results, legal activity PDF report',
    'description': """
Litigation
==========

Legal cases and pre-litigation: cases and parties, domains, procedural deadlines with alerts, fees and honoraries, decisions and results, legal activity PDF report

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
    'data': ['security/litigation_security.xml', 'security/ir.model.access.csv', 'views/litigation_views.xml', 'views/litigation_reports.xml', 'views/res_config_settings_views.xml', 'views/litigation_menus.xml', 'data/litigation_data.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
