# -*- coding: utf-8 -*-
{
    'name': 'Agriculture Management & Farm Operations',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Farms, plots, campaigns, cultures, treatments, harvests and inputs register for agriculture',
    'description': """
Agriculture Management & Farm Operations
========================================

Manage farms and cooperatives: farms and plots (surface, soil),
agricultural campaigns, cultures and technical itineraries,
treatments (crop protection, fertilizers) with withdrawal periods,
harvests with yield computation, inputs register and campaign
reports in PDF.

Key Features:
-------------
* Farm and plot reference data (surface in hectares, soil, irrigation)
* Agricultural campaigns with cultures assigned to plots
* Technical itineraries (operations) per culture
* Treatments with withdrawal periods and automated alerts
* Harvests with yield calculation (t/ha)
* Inputs register and campaign reports in PDF
* Dashboard of yields by crop

Ideal for:
* Farm managers and cooperatives
* Agronomists and technical advisors
* Quality and audit departments (PAC)
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/agri_security.xml',
        'security/ir.model.access.csv',
        'views/agri_views.xml',
        'views/agri_reports.xml',
        'views/res_config_settings_views.xml',
        'views/agri_menus.xml',
        'data/agri_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}