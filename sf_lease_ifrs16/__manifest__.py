{
    'name': 'Lease Accounting (IFRS 16 / ASC 842)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Right-of-use assets, lease liabilities, PV schedules, monthly journal entries and modifications - IFRS 16 & ASC 842',
    'description': """
Lease Ifrs16
============

Right-of-use assets, lease liabilities, PV schedules, monthly journal entries and modifications - IFRS 16 & ASC 842

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
    'depends': ['base', 'account', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/lease_security.xml', 'data/lease_data.xml', 'views/lease_views.xml', 'views/lease_reports.xml'],
    'images': ['static/description/banner.png'],
    'demo': ['data/lease_demo.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
