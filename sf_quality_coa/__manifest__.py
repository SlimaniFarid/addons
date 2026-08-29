{
    'name': 'Certificate of Analysis (CoA) Generator',
    'version': '18.0.1.0.0',
    'category': 'Quality/Quality',
    'summary': 'Generate certificates of analysis per delivery: test parameters, specifications, results and approval workflow',
    'description': """
Quality Coa
===========

Generate certificates of analysis per delivery: test parameters, specifications, results and approval workflow

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
    'depends': ['base', 'stock', 'quality', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/coa_security.xml', 'data/coa_data.xml', 'views/coa_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
