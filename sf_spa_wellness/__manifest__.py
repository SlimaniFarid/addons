{
    'name': 'Spa & Wellness Center Management',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Complete spa management: resource planning, therapists, treatments, packages, memberships',
    'description': """
Spa Wellness
============

Complete spa management: resource planning, therapists, treatments, packages, memberships

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
    'depends': ['base', 'mail', 'contacts', 'account', 'hr', 'product'],
    'data': ['security/sf_spa_wellness_security.xml', 'security/ir.model.access.csv', 'data/sf_spa_wellness_sequence.xml', 'data/sf_spa_wellness_cron.xml', 'data/sf_spa_wellness_report.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}
