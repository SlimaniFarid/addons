{
    'name': 'CAPEX Request & Investment Approval',
    'version': '19.0.1.0.0',
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
    'price': 6.95,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/capex_security.xml', 'data/capex_data.xml', 'views/capex_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
