{
    'name': 'Supplier Rebates & Retro-discounts',
    'version': '19.0.1.0.0',
    'category': 'Purchase/Purchase',
    'summary': 'Vendor rebate deals (volume bonus, retro %), automatic accrual from posted bills, claims and settlement tracking',
    'description': """
Supplier Rebates
================

Vendor rebate deals (volume bonus, retro %), automatic accrual from posted bills, claims and settlement tracking

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
    'depends': ['base', 'account', 'purchase', 'product', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/rebate_security.xml', 'data/rebate_data.xml', 'views/rebate_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
