{
    'name': 'Courier & Parcel Delivery Management',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Pickup/delivery requests, courier assignment, routes, delivery proof (photo/signature), failures, returns and invoicing',
    'description': """
Courier Delivery
================

Pickup/delivery requests, courier assignment, routes, delivery proof (photo/signature), failures, returns and invoicing

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
    'data': ['security/sf_courier_security.xml', 'security/ir.model.access.csv', 'data/sf_courier_sequence.xml', 'data/sf_courier_cron.xml', 'data/sf_courier_report.xml', 'views/sf_courier_order_views.xml', 'views/sf_courier_delivery_views.xml', 'views/sf_courier_route_views.xml', 'views/sf_courier_menus.xml', 'views/report_delivery_ticket.xml', 'views/report_collection_note.xml', 'views/report_disputes_list.xml', 'views/report_activity.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
