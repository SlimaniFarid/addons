# -*- coding: utf-8 -*-
{
    'name': 'Fuel & Fleet Management',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Fuel cards, fills with L/100km consumption tracking, tanks with receipts and anomaly alerts',
    'description': """
Fuel & Fleet Management
=======================

Manage the vehicle fuel fleet: vehicles and fuel cards, fills
(volume, price, mileage) with automatic L/100km consumption
calculation, tanks with gauge and receipts per site, anomaly
alerts (consumption above threshold, cards near expiry) and
monthly PDF reports per vehicle.

Key Features:
-------------
* Vehicle and fuel card registry (diesel, gasoline, electric, LPG...)
* Fuel fills with automatic total and L/100km consumption
* Tanks with current level and receipts per site
* Daily cron alerts: cards near expiry and abnormal fills
* Manager-only card blocking and fill validation
* Monthly consumption PDF report per vehicle
* Tank monitoring PDF report
* Multi-company record rules and dashboard by vehicle

Ideal for:
* Fleet managers and transport teams
* General services and treasury departments
* Fuel stations and internal depots
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/fuel_security.xml',
        'security/ir.model.access.csv',
        'views/fuel_views.xml',
        'views/fuel_reports.xml',
        'views/res_config_settings_views.xml',
        'views/fuel_menus.xml',
        'data/fuel_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
