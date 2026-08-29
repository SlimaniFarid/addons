{
    'name': 'Employee Onboarding & Offboarding',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Structured onboarding and offboarding journeys with checklists, tasks and alerts',
    'description': """
Hr Onboarding
=============

Structured onboarding and offboarding journeys with checklists, tasks and alerts

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
    'depends': ['base', 'hr'],
    'data': ['security/onboarding_security.xml', 'security/ir.model.access.csv', 'views/onboarding_menus.xml', 'views/onboarding_views.xml', 'data/onboarding_cron.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
