{
    'name': 'Quality Alert Aging Monitor',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Monitor open quality alerts by age with escalation at thresholds.',
    'description': """
Quality Alert Aging
===================

Monitor open quality alerts by age with escalation at thresholds.

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
    'banner': 'static/description/banner.png',
    'price': 29.95,
    'currency': 'EUR',
    'depends': ['base', 'quality', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/security.xml', 'data/data.xml', 'views/views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
