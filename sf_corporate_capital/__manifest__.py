{
    'name': 'Shareholder Register & Capital Management (Cap Table)',
    'version': '18.0.1.0',
    'category': 'Accounting',
    'summary': 'Shareholders, share classes, capital movements (issue/transfer/buyback), issued shares, cap table and share certificates',
    'description': """
Corporate Capital
=================

Shareholders, share classes, capital movements (issue/transfer/buyback), issued shares, cap table and share certificates

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
    'depends': ['base', 'mail', 'contacts'],
    'data': ['security/sf_corporate_capital_security.xml', 'security/ir.model.access.csv', 'data/sf_corporate_capital_sequence.xml', 'data/sf_corporate_capital_report.xml', 'views/sf_shareholder_views.xml', 'views/sf_share_class_views.xml', 'views/sf_capital_movement_views.xml', 'views/sf_corporate_capital_menus.xml', 'views/sf_corporate_capital_settings_views.xml', 'views/report_cap_table.xml', 'views/report_share_certificate.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
