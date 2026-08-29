{
    'name': 'Corporate Business Travel Management',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Employee travel requests, approval workflow, itinerary lines, budget tracking and mission orders',
    'description': """
Business Travel
===============

Employee travel requests, approval workflow, itinerary lines, budget tracking and mission orders

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
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/sf_business_travel_security.xml', 'security/ir.model.access.csv', 'data/sf_business_travel_sequence.xml', 'data/sf_business_travel_cron.xml', 'data/sf_business_travel_report.xml', 'views/sf_business_travel_views.xml', 'views/sf_business_travel_menus.xml', 'views/report_travel_authorization.xml', 'views/report_travel_itinerary.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
