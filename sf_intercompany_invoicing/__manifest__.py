{
    'name': 'Intercompany Invoicing Automation',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Automated intercompany invoices with multi-book accounting, currency conversion and elimination entries.',
    'description': """
Intercompany Invoicing
======================

Automated intercompany invoices with multi-book accounting, currency conversion and elimination entries.

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
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock', 'sale'],
    'data': ['security/sf_intercompany_invoicing_security.xml', 'security/ir.model.access.csv', 'data/sf_intercompany_invoicing_sequence.xml', 'views/ic_sale_views.xml', 'views/sf_intercompany_invoicing_menus.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
