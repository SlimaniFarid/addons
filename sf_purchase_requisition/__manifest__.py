{
    'name': 'Purchase Requisition Workflow',
    'version': '19.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Purchase requisition with multi-level approval chains, budget checking and vendor suggestion.',
    'description': """
Purchase Requisition
====================

Purchase requisition with multi-level approval chains, budget checking and vendor suggestion.

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
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock', 'hr', 'purchase'],
    'data': ['security/sf_purchase_requisition_security.xml', 'security/ir.model.access.csv', 'data/sf_purchase_requisition_sequence.xml', 'views/purchase_requisition_sf_views.xml', 'views/requisition_line_views.xml', 'views/sf_purchase_requisition_menus.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
