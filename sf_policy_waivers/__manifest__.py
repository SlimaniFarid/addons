{
    'name': 'Policy Exception & Waiver Management',
    'version': '19.0.1.0.0',
    'category': 'Human Resources/Employees',
    'summary': 'Time-boxed policy waivers with risk assessment, compensating controls and approval workflow',
    'description': """
Policy Waivers
==============

Time-boxed policy waivers with risk assessment, compensating controls and approval workflow

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
    'price': 6.95,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/pw_security.xml', 'data/pw_data.xml', 'views/pw_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
