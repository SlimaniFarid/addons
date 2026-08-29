{
    'name': 'Salon & Beauty Studio Management',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Appointments, staff availability, packages, commissions and billing for salons and beauty studios',
    'description': """
Salon Beauty
============

Appointments, staff availability, packages, commissions and billing for salons and beauty studios

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
    'data': ['security/sf_salon_security.xml', 'security/ir.model.access.csv', 'data/sf_salon_sequence.xml', 'data/sf_salon_cron.xml', 'data/sf_salon_report.xml', 'views/sf_salon_service_views.xml', 'views/sf_salon_staff_views.xml', 'views/sf_salon_appointment_views.xml', 'views/sf_salon_package_views.xml', 'views/sf_salon_commission_views.xml', 'views/sf_salon_menus.xml', 'views/report_customer_card.xml', 'views/report_commissions.xml', 'views/report_activity.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
