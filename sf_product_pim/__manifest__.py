{
    'name': 'PIM - Product Information Management',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Central product data, families, attributes, completeness score and channel publications',
    'description': """
Product Pim
===========

Central product data, families, attributes, completeness score and channel publications

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
    'depends': ['base', 'product', 'mail'],
    'data': ['security/pim_security.xml', 'security/ir.model.access.csv', 'data/pim_data.xml', 'views/pim_views.xml', 'views/pim_product_views.xml', 'views/res_config_settings_views.xml', 'views/pim_menus.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
