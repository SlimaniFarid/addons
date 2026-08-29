{
    'name': 'Parking Lot & Garage Management',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Parking sites and zones, spaces, recurring subscriptions, tickets, entry/exit and occupancy statistics',
    'description': """
Parking Management
==================

Parking sites and zones, spaces, recurring subscriptions, tickets, entry/exit and occupancy statistics

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
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_parking_security.xml', 'security/ir.model.access.csv', 'data/sf_parking_sequence.xml', 'data/sf_parking_cron.xml', 'data/sf_parking_report.xml', 'views/sf_parking_site_views.xml', 'views/sf_parking_ticket_views.xml', 'views/sf_parking_subscription_views.xml', 'views/sf_parking_report_wizard_views.xml', 'views/sf_parking_menus.xml', 'views/report_ticket.xml', 'views/report_subscription.xml', 'views/report_revenue.xml', 'views/report_occupancy.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
