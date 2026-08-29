{
    'name': 'Electronic Batch Production Records (EBR)',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Electronic batch production records: materials, steps, parameters, deviations, QA review and lot release',
    'description': """
Batch Records
=============

Electronic batch production records: materials, steps, parameters, deviations, QA review and lot release

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
    'depends': ['base', 'mail', 'product', 'stock', 'contacts'],
    'data': ['security/sf_batch_records_security.xml', 'security/ir.model.access.csv', 'data/sf_batch_records_sequence.xml', 'data/sf_batch_records_report.xml', 'views/sf_batch_record_views.xml', 'views/sf_batch_records_menus.xml', 'views/report_batch_record.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
