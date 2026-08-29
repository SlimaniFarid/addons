{
    'name': 'Trade Promotion Management (TPM)',
    'version': '18.0.1.0',
    'category': 'Sales',
    'summary': 'Trade promotion programs, budgets, customer claims, validation workflow and ROI tracking',
    'description': """
Trade Promotions
================

Trade promotion programs, budgets, customer claims, validation workflow and ROI tracking

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
    'data': ['security/sf_trade_promotions_security.xml', 'security/ir.model.access.csv', 'data/sf_trade_promotions_sequence.xml', 'data/sf_trade_promotions_cron.xml', 'data/sf_trade_promotions_report.xml', 'views/sf_trade_program_views.xml', 'views/sf_trade_claim_views.xml', 'views/sf_trade_promotions_menus.xml', 'views/report_trade_program.xml', 'views/report_trade_claim.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
