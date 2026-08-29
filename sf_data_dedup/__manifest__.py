{
    'name': 'Duplicate Records Audit & Merge Assistant',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Detect duplicate partners (name, email, VAT) with similarity scoring, review groups and track merges',
    'description': """
Data Dedup
==========

Detect duplicate partners (name, email, VAT) with similarity scoring, review groups and track merges

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
    'data': ['security/ir.model.access.csv', 'security/dedup_security.xml', 'data/dedup_data.xml', 'views/dedup_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
