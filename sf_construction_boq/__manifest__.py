{
    'name': 'Construction BOQ & Subcontractor Billing',
    'version': '18.0.1.0',
    'category': 'Operations/Project',
    'summary': 'Bill of Quantities, subcontract management and progress billing (IPC) for construction',
    'description': """
Construction Boq
================

Bill of Quantities, subcontract management and progress billing (IPC) for construction

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
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'project', 'product', 'account', 'uom'],
    'data': ['security/construction_security.xml', 'security/ir.model.access.csv', 'data/construction_sequences.xml', 'views/construction_menus.xml', 'views/construction_views.xml', 'reports/certificate_report.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
