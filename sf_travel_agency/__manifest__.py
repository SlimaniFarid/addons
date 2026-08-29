{
    'name': 'SF Travel Agency',
    'version': '18.0.1.0',
    'category': 'Sales',
    'summary': 'Manage travel packages, providers, reservations and margin analysis.',
    'description': """
Travel Agency
=============

Manage travel packages, providers, reservations and margin analysis.

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
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_travel_agency_security.xml', 'security/ir.model.access.csv', 'data/data.xml', 'data/reports.xml', 'views/sf_travel_package_views.xml', 'views/sf_travel_provider_views.xml', 'views/sf_travel_reservation_views.xml', 'views/sf_travel_provider_cost_views.xml', 'views/res_config_settings_views.xml', 'views/report_reservation_confirmation.xml', 'views/report_package_itinerary.xml', 'views/report_reservation_invoice.xml', 'views/report_margin_report.xml', 'views/sf_travel_menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
