{
    'name': 'WhatsApp Business API',
    'version': '18.0.1.0',
    'category': 'Productivity',
    'summary': 'Send WhatsApp messages from Odoo via Meta Cloud API',
    'description': """
Whatsapp Cloud Api
==================

Send WhatsApp messages from Odoo via Meta Cloud API

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
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'sale', 'account', 'stock'],
    'data': ['security/ir.model.access.csv', 'views/whatsapp_menus.xml', 'data/whatsapp_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
