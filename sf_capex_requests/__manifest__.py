{
    'name': 'CAPEX Request & Investment Approval',
    'version': '18.0.1.0.0',
    'category': 'Finance/Finance',
    'summary': 'Capital expenditure requests with multi-level approvals, ROI/payback fields, budget check and capitalization tracking',
    'description': """
Capex Requests
==============

Capital expenditure requests with multi-level approvals, ROI/payback fields, budget check and capitalization tracking

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
    'depends': ['base', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/capex_security.xml', 'data/capex_data.xml', 'views/capex_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
