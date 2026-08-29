{
    'name': 'Energy Meter Readings & Alerts',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Monthly meter readings per site with consumption trends and anomaly alerts.',
    'description': """
Energy Meter Readings
=====================

Monthly meter readings per site with consumption trends and anomaly alerts.

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
    'images': ['static/description/banner.png'],
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/security.xml', 'data/data.xml', 'views/views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
