{
    'name': 'E-commerce Digital Goods & License Key Delivery',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Digital products, automatic license key generation, expirable download links and digital delivery tracking',
    'description': """
Digital Delivery
================

Digital products, automatic license key generation, expirable download links and digital delivery tracking

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
    'depends': ['base', 'mail', 'contacts', 'product', 'sale'],
    'data': ['security/sf_digital_delivery_security.xml', 'security/ir.model.access.csv', 'data/sf_digital_delivery_sequence.xml', 'data/sf_digital_delivery_cron.xml', 'data/sf_digital_delivery_report.xml', 'views/sf_digital_delivery_product_views.xml', 'views/sf_digital_delivery_key_views.xml', 'views/sf_digital_delivery_delivery_views.xml', 'views/sf_digital_delivery_menus.xml', 'views/report_digital_delivery.xml', 'views/report_license_key.xml', 'views/res_config_settings_views.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}
