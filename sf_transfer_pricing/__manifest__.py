{
    'name': 'Transfer Pricing Engine & OECD Documentation',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Intercompany arm-length pricing policies (CUP, cost-plus, resale-minus, TNMM), variance analysis and Master File / Local File documentation',
    'description': """
Transfer Pricing
================

Intercompany arm-length pricing policies (CUP, cost-plus, resale-minus, TNMM), variance analysis and Master File / Local File documentation

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
    'depends': ['base', 'account', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/tp_security.xml', 'data/tp_data.xml', 'views/tp_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
