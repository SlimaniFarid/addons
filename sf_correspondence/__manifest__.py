{
    'name': 'Business Mail & Correspondence Register',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Incoming and outgoing correspondence register with routing, response deadlines and registered mail tracking',
    'description': """
Correspondence
==============

Incoming and outgoing correspondence register with routing, response deadlines and registered mail tracking

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
    'data': ['security/sf_correspondence_security.xml', 'security/ir.model.access.csv', 'data/sf_correspondence_sequence.xml', 'data/sf_correspondence_cron.xml', 'data/sf_correspondence_report.xml', 'views/sf_correspondence_views.xml', 'views/sf_correspondence_department_views.xml', 'views/sf_correspondence_menus.xml', 'views/report_correspondence_register.xml', 'views/report_correspondence_sheet.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
