{
    'name': 'First-Piece Validation',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/MES',
    'summary': 'First-piece validation per setup: measurements, checklist and production release gate.',
    'description': """
First Piece Validation
======================

First-piece validation per setup: measurements, checklist and production release gate.

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
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mrp', 'quality', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/security.xml', 'data/data.xml', 'views/views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
