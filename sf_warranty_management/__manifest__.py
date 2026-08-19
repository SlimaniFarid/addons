# -*- coding: utf-8 -*-
{
    'name': 'Warranty & Claims Management',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Product warranties, claims with automatic eligibility check and motivated decisions',
    'description': """
Warranty & Claims Management
============================

Centralize product warranties (duration, coverage), activate them
at sale and process customer claims with automatic eligibility
verification (serial number, purchase date), motivated decisions
(accepted / rejected / exception) and warranty cost tracking.

Key Features:
------------
* Warranty catalog per product (duration, coverage)
* Claims workflow: draft → open → decision → closed / rejected
* Automatic eligibility check (serial number + purchase date)
* Motivated decisions with mandatory reason on rejection
* Estimated warranty cost per claim
* Warranty page on the product form
* Dashboard of claims by state and decision

Ideal for:
* After-sales service teams
* Manufacturers, equipment and B2B distributors
* Quality departments
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 57.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'product', 'stock', 'sale', 'account'],
    'data': [
        'security/warranty_security.xml',
        'security/ir.model.access.csv',
        'views/warranty_views.xml',
        'views/warranty_reports.xml',
        'views/res_config_settings_views.xml',
        'views/warranty_menus.xml',
        'data/warranty_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}