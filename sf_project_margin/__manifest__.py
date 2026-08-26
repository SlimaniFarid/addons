{
    'name': 'Project Margin & Budget Control',
    'version': '19.0.1.0.0',
    'category': 'Project/Project',
    'summary': 'Track project budgets, costs and margins live',
    'description': """
Project Margin
==============

Track project budgets, costs and margins live

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
    'depends': ['base', 'project', 'sale', 'account'],
    'data': ['security/project_margin_security.xml', 'security/ir.model.access.csv', 'views/project_margin_menus.xml', 'views/project_margin_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
