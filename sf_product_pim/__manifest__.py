# -*- coding: utf-8 -*-
{
    'name': 'PIM - Product Information Management',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Central product data, families, attributes, completeness score and channel publications',
    'description': """
PIM - Product Information Management
=====================================

Central reference for all product information: families and
enriched attributes, product translations, media management,
validation and publication workflow per channel (web,
marketplace, catalogue), completeness and quality control of
product sheets, syndication of validated sheets to target
channels. Integrated with Odoo products (product.template).

Key Features:
-------------
* Product families and structured attributes
* Product completeness score with configurable threshold
* Validation workflow (draft / in_review / approved / published / archived)
* Publication per channel with reversible withdrawal
* Product translations by language
* Review history and quality dashboard

Ideal for:
* Product management and marketing teams
* E-commerce managers
* Data stewards and reference data teams
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 65.00,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'product', 'mail'],
    'data': [
        'security/pim_security.xml',
        'security/ir.model.access.csv',
        'data/pim_data.xml',
        'views/pim_views.xml',
        'views/pim_product_views.xml',
        'views/res_config_settings_views.xml',
        'views/pim_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
