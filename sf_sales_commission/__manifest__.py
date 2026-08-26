{
    'name': 'Sales Commission Engine',
    'version': '18.0.1.0',
    'category': 'Sales',
    'summary': 'Flexible commission plans, auto-computed from paid invoices and tracked per salesperson',
    'description': """
Sales Commission
================

Flexible commission plans, auto-computed from paid invoices and tracked per salesperson

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
    'depends': ['base', 'sale', 'account'],
    'data': ['security/commission_security.xml', 'security/ir.model.access.csv', 'views/commission_views.xml', 'views/sale_order_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
