{
    'name': 'Mental Health & Therapy Practice Management',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Mental health practice: patient records, treatment plans, sessions, billing, outcomes',
    'description': """
Mental Health
=============

Mental health practice: patient records, treatment plans, sessions, billing, outcomes

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
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_mental_health_security.xml', 'security/ir.model.access.csv', 'data/sf_mental_health_sequence.xml', 'data/sf_mental_health_cron.xml', 'data/sf_mental_health_report.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}
