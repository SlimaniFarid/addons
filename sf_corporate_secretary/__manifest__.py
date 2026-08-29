{
    'name': 'Corporate Secretary & Corporate Life',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Corporate secretariat: organs, AG/board meetings, convocations, resolutions, votes, minutes, written decisions and regulatory deadlines',
    'description': """
Corporate Secretary
===================

Corporate secretariat: organs, AG/board meetings, convocations, resolutions, votes, minutes, written decisions and regulatory deadlines

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
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/corporate_security.xml', 'security/ir.model.access.csv', 'views/corporate_views.xml', 'views/corporate_reports.xml', 'views/res_config_settings_views.xml', 'views/corporate_menus.xml', 'data/corporate_data.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
