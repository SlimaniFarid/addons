# -*- coding: utf-8 -*-
{
    'name': 'Waste Management (BSD)',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'sequence': 12,
    'summary': 'Waste tracking slips (BSD), sites and waste codes',
    'description': 'Manage waste tracking slips (BSD) with sites, waste '
                   'codes, collectors, and a full emission, transfer and '
                   'reception workflow.',
    'author': 'Ethan Miller',
    'license': 'OPL-1',
    'website': 'https://tech5262@gmail.com',
    'support': 'tech5262@gmail.com',
    'depends': ['base', 'mail', 'contacts', 'web'],
    'data': [
        'security/waste_groups.xml',
        'security/ir.model.access.csv',
        'data/waste_data.xml',
        'views/waste_views.xml',
        'views/waste_reports.xml',
        'views/waste_menus.xml',
        'views/res_config_settings_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'price': 45.00,
}
