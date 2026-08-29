{
    'name': 'Field Dispatch Board',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Dispatch board with skills matching, route optimization, SLA timers and mobile check-in/out.',
    'description': """
Field Dispatch Board
====================

Dispatch board with skills matching, route optimization, SLA timers and mobile check-in/out.

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
    'data': ['security/sf_field_dispatch_board_security.xml', 'security/ir.model.access.csv', 'data/sf_field_dispatch_board_sequence.xml', 'views/dispatch_ticket_views.xml', 'views/sf_field_dispatch_board_menus.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
