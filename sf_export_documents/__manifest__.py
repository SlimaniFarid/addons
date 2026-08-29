{
    'name': 'Export Documents & Customs Compliance',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Export pack documents, Incoterms, completeness control and dossier workflow',
    'description': """
Export Documents
================

Export pack documents, Incoterms, completeness control and dossier workflow

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
    'depends': ['base', 'mail', 'contacts', 'sale', 'product'],
    'data': ['security/export_security.xml', 'security/ir.model.access.csv', 'views/export_views.xml', 'views/export_reports.xml', 'views/res_config_settings_views.xml', 'views/export_menus.xml', 'data/export_data.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
