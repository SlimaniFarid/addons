{
    'name': 'Credit & Debt Collection',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Aging analysis, collection cases, dunning plans and payment promises',
    'description': """
Debt Collection
===============

Aging analysis, collection cases, dunning plans and payment promises

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
    'price': 29.95,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': ['security/debt_security.xml', 'security/ir.model.access.csv', 'data/debt_data.xml', 'views/debt_menus.xml', 'views/debt_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
