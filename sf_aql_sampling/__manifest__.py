{
    'name': 'Acceptance Sampling & AQL Inspection Plans',
    'version': '18.0.1.0',
    'category': 'Quality/Quality',
    'summary': 'Statistical acceptance sampling: AQL inspection plans, lot inspections, defect recording and accept/reject decisions',
    'description': """
Aql Sampling
============

Statistical acceptance sampling: AQL inspection plans, lot inspections, defect recording and accept/reject decisions

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
    'depends': ['base', 'mail', 'product', 'stock', 'contacts'],
    'data': ['security/sf_aql_sampling_security.xml', 'security/ir.model.access.csv', 'data/sf_aql_sampling_sequence.xml', 'data/sf_aql_sampling_report.xml', 'views/sf_aql_plan_views.xml', 'views/sf_aql_inspection_views.xml', 'views/sf_aql_sampling_menus.xml', 'views/report_aql_inspection.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
