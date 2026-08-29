{
    'name': 'Customer Rebates & Turnover Bonuses',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Sell-side rebate deals (retro %, turnover bonus, per unit) with accrual from invoices and credit note settlement',
    'description': """
Customer Rebates
================

Sell-side rebate deals (retro %, turnover bonus, per unit) with accrual from invoices and credit note settlement

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
    'depends': ['base', 'account', 'sale', 'product', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/crebate_security.xml', 'data/crebate_data.xml', 'views/crebate_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
