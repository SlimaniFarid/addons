{
    'name': 'Restaurant, Cafe & In-Room Dining',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Restaurant and cafe management: tables, reservations, menus, kitchen orders and revenue tracking',
    'description': """
Restaurant
==========

Restaurant and cafe management: tables, reservations, menus, kitchen orders and revenue tracking

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
    'depends': ['base', 'mail', 'contacts', 'product'],
    'data': ['security/sf_restaurant_security.xml', 'security/ir.model.access.csv', 'data/sf_restaurant_sequence.xml', 'data/sf_restaurant_cron.xml', 'data/sf_restaurant_report.xml', 'views/sf_restaurant_table_views.xml', 'views/sf_restaurant_zone_views.xml', 'views/sf_restaurant_reservation_views.xml', 'views/sf_restaurant_menu_category_views.xml', 'views/sf_restaurant_menu_item_views.xml', 'views/sf_restaurant_order_views.xml', 'views/sf_restaurant_menus.xml', 'views/report_kitchen_ticket.xml', 'views/report_table_bill.xml', 'views/report_daily_revenue.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}
