{
    'name': 'Customer Credit Limits',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Automated credit limit enforcement with blocking, escalation workflow and exposure dashboard.',
    'description': """
Customer Credit Limits
======================

Automated credit limit enforcement with blocking, escalation workflow and exposure dashboard.

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
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': ['security/sf_customer_credit_limits_security.xml', 'security/ir.model.access.csv', 'data/sf_customer_credit_limits_sequence.xml', 'views/credit_limit_rule_views.xml', 'views/credit_exposure_views.xml', 'views/sf_customer_credit_limits_menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
