{
    'name': 'Membership & Associations',
    'version': '19.0.1.0.0',
    'category': 'Website',
    'summary': 'Manage members, subscriptions & renewals for associations and NGOs',
    'description': """
Membership Advanced
===================

Manage members, subscriptions & renewals for associations and NGOs

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
    'depends': ['base', 'mail', 'sale', 'account', 'website'],
    'data': ['security/ir.model.access.csv', 'views/membership_menus.xml', 'views/membership_plan_views.xml', 'views/membership_member_views.xml', 'views/membership_subscription_views.xml', 'views/membership_payment_views.xml', 'data/membership_data.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
