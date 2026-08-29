{
    'name': 'Training & Certification Tracking',
    'version': '18.0.1.0',
    'category': 'Human Resources',
    'summary': 'Track employee trainings, sessions, registrations and certifications with expiry alerts',
    'description': """
Training Certifications
=======================

Track employee trainings, sessions, registrations and certifications with expiry alerts

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
    'price': 29.95,
    'currency': 'EUR',
    'depends': ['base', 'hr', 'mail'],
    'data': ['data/training_data.xml', 'data/training_cron.xml', 'security/training_security.xml', 'security/ir.model.access.csv', 'views/training_menus.xml', 'views/training_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
    'auto_install': False,
}
