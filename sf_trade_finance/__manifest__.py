# -*- coding: utf-8 -*-
{
    'name': 'Trade Finance — LC & Bank Guarantees',
    'version': '18.0.1.0',
    'category': 'Finance',
    'summary': 'Letters of credit, bank guarantees and documentary collections with key dates and documents',
    'description': """
Trade Finance — LC & Bank Guarantees
====================================

Manage international documentary payment instruments:
letters of credit (import/export), bank guarantees and
documentary collections. Track key dates (application, issue,
expiry, payment) with alerts, required documents and their
status, links to purchase orders and invoices, and a register of
bank fees.

Key Features:
-------------
* Import/export letters of credit, guarantees, collections
* Key dates tracking with expiry alerts (daily cron)
* Required documents with submit / accept / reject workflow
* Bank fees register per instrument
* Links to purchase orders and invoices
* Dashboard of outstanding amounts and expiring instruments

Ideal for:
* Treasury and finance teams
* International buyers and export sales teams
* Financial controllers
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 52.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'purchase', 'account', 'mail'],
    'data': [
        'security/trade_security.xml',
        'security/ir.model.access.csv',
        'views/trade_views.xml',
        'views/res_config_settings_views.xml',
        'views/trade_menus.xml',
        'data/trade_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}