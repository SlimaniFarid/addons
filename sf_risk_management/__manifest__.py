{
    'name': 'GRC — Enterprise Risk Management',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Risk register, 5x5 matrix, treatment plans, controls and regulatory mapping',
    'description': """
Risk Management
===============

Risk register, 5x5 matrix, treatment plans, controls and regulatory mapping

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
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'hr'],
    'data': ['security/risk_security.xml', 'security/ir.model.access.csv', 'views/risk_menus.xml', 'views/risk_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
