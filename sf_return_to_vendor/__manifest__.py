{
    'name': 'Return to Vendor (RTV) & Supplier Returns',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Defective and excess goods returns to suppliers: RTV orders with dispositions (return/credit/replace/scrap), return pickings and debit note tracking',
    'description': """
Return To Vendor
================

Defective and excess goods returns to suppliers: RTV orders with dispositions (return/credit/replace/scrap), return pickings and debit note tracking

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
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'stock', 'purchase', 'account', 'mail'],
    'data': ['security/ir.model.access.csv', 'security/rtv_security.xml', 'data/rtv_data.xml', 'views/rtv_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
