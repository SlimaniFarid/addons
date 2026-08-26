{
    'name': 'Senior Living & Retirement Community Management',
    'version': '18.0.1.0',
    'category': 'Healthcare',
    'summary': 'Complete management for senior residences, EHPAD, retirement communities',
    'description': """
Senior Living
=============

Complete management for senior residences, EHPAD, retirement communities

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
    'data': ['security/sf_senior_living_security.xml', 'security/ir.model.access.csv', 'data/sf_senior_living_sequence.xml', 'views/sf_senior_residence_views.xml', 'views/sf_senior_menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
