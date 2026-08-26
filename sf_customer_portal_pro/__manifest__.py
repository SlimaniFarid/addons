{
    'name': 'Customer Self-Service Portal Pro',
    'version': '18.0.1.0',
    'category': 'Website',
    'summary': 'B2B/B2C portal: invoices, payments, subscriptions, returns, tickets, documents',
    'description': """
Customer Portal Pro
===================

B2B/B2C portal: invoices, payments, subscriptions, returns, tickets, documents

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
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'website', 'sale', 'account', 'portal', 'payment'],
    'data': ['security/ir.model.access.csv', 'views/portal_menus.xml', 'data/portal_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
