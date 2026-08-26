{
    'name': 'Business Continuity & BIA (PCA)',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Resilience ISO 22301: critical processes BIA, continuity strategies, recovery plans, exercises and review alerts',
    'description': """
Business Continuity
===================

Resilience ISO 22301: critical processes BIA, continuity strategies, recovery plans, exercises and review alerts

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
    'data': ['security/bcp_security.xml', 'security/ir.model.access.csv', 'views/bcp_views.xml', 'views/bcp_reports.xml', 'views/res_config_settings_views.xml', 'views/bcp_menus.xml', 'data/bcp_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
