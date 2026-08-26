{
    'name': 'Laundry & Dry Cleaning Management',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Deposit vouchers and items, treatment statuses, per-piece pricing, pickup/delivery and customer history',
    'description': """
Laundry
=======

Deposit vouchers and items, treatment statuses, per-piece pricing, pickup/delivery and customer history

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
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_laundry_security.xml', 'security/ir.model.access.csv', 'data/sf_laundry_sequence.xml', 'data/sf_laundry_cron.xml', 'data/sf_laundry_report.xml', 'views/sf_laundry_order_views.xml', 'views/sf_laundry_item_views.xml', 'views/sf_laundry_item_type_views.xml', 'views/sf_laundry_menus.xml', 'views/report_deposit_receipt.xml', 'views/report_delivery_ticket.xml', 'views/report_activity.xml', 'views/report_overdue_list.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
