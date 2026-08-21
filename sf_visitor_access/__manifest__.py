# -*- coding: utf-8 -*-
{
    'name': 'Visitor Management & Site Access',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Visitor check-in/out, badges, zones, safety rules and real-time presence register',
    'description': """
Visitor Management & Site Access
================================

Manage visitors and contractors on site: check-in / check-out,
visit types, badges and authorized zones, accepted safety rules
(waiver), overtime alerts, real-time presence register, list of
people on site (evacuation) and site history. Integrated with
employees (hr).

Key Features:
-------------
* Visitor register with check-in / check-out
* Unique badge generation and authorized zones
* Safety rules acceptance (waiver) per site version
* Overtime alerts via cron (configurable threshold)
* Real-time "Present on site" list for evacuation
* Known recurring visitors
* Dashboard of visits by type and gate

Ideal for:
* Reception and security teams
* Site managers and QHSE
* Industrial sites, offices and worksites
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 42.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/visitor_security.xml',
        'security/ir.model.access.csv',
        'views/visitor_views.xml',
        'views/res_config_settings_views.xml',
        'views/visitor_menus.xml',
        'data/visitor_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}