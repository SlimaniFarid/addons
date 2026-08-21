# -*- coding: utf-8 -*-
{
    'name': 'Pharmacy & Dispensation Management',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Pharmacy management: products, batches, expiries and prescription dispensations',
    'description': 'Pharmacy management module: pharmaceutical products, batch stock with expiry dates, stock-out and expiry alerts, traced prescription dispensations, batch recalls and stock movements.',
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'application': True,
    'installable': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_pharmacy_security.xml',
        'security/ir.model.access.csv',
        'views/sf_pharmacy_views.xml',
        'views/res_config_settings_views.xml',
        'views/sf_pharmacy_reports.xml',
        'data/actions.xml',
    ],
}

