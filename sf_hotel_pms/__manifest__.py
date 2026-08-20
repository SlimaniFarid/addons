# -*- coding: utf-8 -*-
{
    'name': 'Hotel PMS',
    'summary': 'Hôtellerie & Réservations (PMS léger)',
    'description': """
Hôtellerie & Réservations (PMS léger)
=====================================

Rooms and types with rates, multi-night reservations without
overbooking, check-in / check-out, additional charged services,
housekeeping and computed night billing, with daily cron alerts on
departures and housekeeping.

Key Features:
-------------
* Room fleet with statuses (available / occupied / maintenance /
  reserved)
* Multi-night reservations with anti-overbooking control
* Check-in / check-out workflow reserved to managers
* Additional charged services (extras)
* Computed nights and stay total (nights x base price + charged
  extras)
* Housekeeping planning and follow-up
* Daily departure and housekeeping alerts via cron (deduplicated)
* Per-company access rules

Ideal for:
* Hotel reception teams
* Hotel management
* Housekeeping teams
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': 'https://tech5262@gmail.com',
    'category': 'Other/Others',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 62.50,
    'application': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_hotel_pms_security.xml',
        'security/ir.model.access.csv',
        'views/sf_hotel_pms_views.xml',
        'views/sf_hotel_pms_reports.xml',
        'views/res_config_settings_views.xml',
        'views/sf_hotel_pms_menus.xml',
        'data/actions.xml',
    ],
    'installable': True,
    'auto_install': False,
}
