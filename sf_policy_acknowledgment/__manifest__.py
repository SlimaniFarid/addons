{
    'name': 'Company Policy & Employee Acknowledgment Register',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Versioned internal policies, employee assignment, acknowledgment sign-off, reminders and coverage rate',
    'description': """
Policy Acknowledgment
=====================

Versioned internal policies, employee assignment, acknowledgment sign-off, reminders and coverage rate

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
    'depends': ['base', 'mail', 'contacts', 'hr'],
    'data': ['security/sf_policy_acknowledgment_security.xml', 'security/ir.model.access.csv', 'data/sf_policy_acknowledgment_sequence.xml', 'data/sf_policy_acknowledgment_cron.xml', 'data/sf_policy_acknowledgment_report.xml', 'views/sf_policy_views.xml', 'views/sf_policy_acknowledgment_views.xml', 'views/sf_policy_acknowledgment_menus.xml', 'views/report_policy.xml', 'views/report_policy_acknowledgment.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
