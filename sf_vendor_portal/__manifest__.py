{
    'name': 'Vendor Portal & e-Procurement',
    'version': '19.0.1.0.0',
    'category': 'Purchasing',
    'summary': 'Self-service vendor portal: RFQs, quotations, orders and invoices online',
    'description': """
Vendor Portal
=============

Self-service vendor portal: RFQs, quotations, orders and invoices online

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
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'purchase', 'portal', 'account', 'mail'],
    'data': ['security/vendor_portal_security.xml', 'security/ir.model.access.csv', 'data/vendor_portal_data.xml', 'views/vendor_portal_menus.xml', 'views/vendor_portal_views.xml', 'views/vendor_portal_templates.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
