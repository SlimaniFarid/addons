{
    'name': 'Staffing Agency & Placement',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Temporary work and placement agency management: candidates, clients, needs, missions, contracts, timesheets and invoicing.',
    'description': """
Staffing
========

Temporary work and placement agency management: candidates, clients, needs, missions, contracts, timesheets and invoicing.

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
    'license': 'OPL-1',
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_staffing_security.xml', 'security/ir.model.access.csv', 'data/sf_staffing_sequence.xml', 'data/sf_staffing_cron.xml', 'data/sf_staffing_report.xml', 'views/sf_staffing_candidate_views.xml', 'views/sf_staffing_client_views.xml', 'views/sf_staffing_need_views.xml', 'views/sf_staffing_mission_views.xml', 'views/sf_staffing_contract_views.xml', 'views/sf_staffing_timesheet_views.xml', 'views/sf_staffing_menus.xml', 'views/report_contract.xml', 'views/report_candidate.xml', 'views/report_mission_invoice.xml', 'views/report_activity.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
