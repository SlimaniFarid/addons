{
    'name': 'Freight Audit',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Audit carrier invoices against contracts and shipments: detect overcharges, manage disputes, recover money',
    'description': """
Freight Audit
=============

Audit carrier invoices against contracts and shipments: detect overcharges, manage disputes, recover money

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
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': ['security/sf_freight_audit_security.xml', 'security/ir.model.access.csv', 'data/sf_freight_audit_sequence.xml', 'data/sf_freight_audit_cron.xml', 'views/sf_freight_contract_views.xml', 'views/sf_freight_invoice_views.xml', 'views/sf_freight_rule_views.xml', 'views/sf_freight_audit_menus.xml', 'report/sf_freight_audit_reports.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
