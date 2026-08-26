{
    'name': 'Product Compliance & Technical Documentation',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Regulatory compliance of products (CE, RoHS, REACH, UL, FDA): regulations, requirements, compliance dossiers and certificates with expiry alerts',
    'description': """
Product Compliance
==================

Regulatory compliance of products (CE, RoHS, REACH, UL, FDA): regulations, requirements, compliance dossiers and certificates with expiry alerts

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
    'depends': ['base', 'mail', 'product', 'contacts'],
    'data': ['security/compliance_security.xml', 'security/ir.model.access.csv', 'views/compliance_views.xml', 'views/compliance_menus.xml', 'views/res_config_settings_views.xml', 'views/compliance_reports.xml', 'data/compliance_data.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
