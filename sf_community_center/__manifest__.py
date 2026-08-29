{
    'name': 'Community Center & Recreation Management',
    'version': '18.0.1.0',
    'category': 'Services',
    'summary': 'Community center management: spaces, activities, memberships, ticketing, grants',
    'description': """
Community Center
================

Community center management: spaces, activities, memberships, ticketing, grants

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
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_community_center_security.xml', 'security/ir.model.access.csv', 'data/sf_community_center_sequence.xml', 'data/sf_community_center_cron.xml', 'data/sf_community_center_report.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
