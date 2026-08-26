{
    'name': 'Change Request & CAB Workflow',
    'version': '18.0.1.0.0',
    'category': 'Operations/Operations',
    'summary': 'IT and operational changes with CAB review, risk levels, rollback plans and post-implementation closure',
    'description': """
Change Requests
===============

IT and operational changes with CAB review, risk levels, rollback plans and post-implementation closure

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
    'depends': ['base', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/cr_security.xml', 'data/cr_data.xml', 'views/cr_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
