{
    'name': 'Customer Health & Churn Risk',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Post-sale health scoring per customer: revenue recency, trend and overdue signals with churn risk rating',
    'description': """
Customer Health
===============

Post-sale health scoring per customer: revenue recency, trend and overdue signals with churn risk rating

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
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'sale', 'account', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/ch_security.xml', 'data/ch_data.xml', 'views/ch_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
