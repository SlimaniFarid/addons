{
    'name': 'Quality Inspection Mobile',
    'version': '18.0.1.0.0',
    'category': 'Quality',
    'summary': 'Mobile-first quality inspection checklists with photo capture and non-conformance escalation.',
    'description': """
Quality Inspection
==================

Mobile-first quality inspection checklists with photo capture and non-conformance escalation.

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
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': ['security/sf_quality_inspection_security.xml', 'security/ir.model.access.csv', 'data/sf_quality_inspection_sequence.xml', 'views/inspection_plan_views.xml', 'views/quality_inspection_views.xml', 'views/sf_quality_inspection_menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
