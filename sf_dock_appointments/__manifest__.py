{
    'name': 'Dock & Shipment Appointment Scheduling',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Dock registry and truck appointment scheduling with time windows, arrival tracking and no-show detection',
    'description': """
Dock Appointments
=================

Dock registry and truck appointment scheduling with time windows, arrival tracking and no-show detection

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
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/sf_dock_appointments_security.xml', 'security/ir.model.access.csv', 'data/sf_dock_appointments_sequence.xml', 'data/sf_dock_appointments_cron.xml', 'data/sf_dock_appointments_report.xml', 'views/sf_dock_views.xml', 'views/sf_dock_appointment_views.xml', 'views/sf_dock_appointments_menus.xml', 'views/report_appointments.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
