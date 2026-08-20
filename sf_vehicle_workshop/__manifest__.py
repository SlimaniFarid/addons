# -*- coding: utf-8 -*-
{
    'name': 'Atelier & Maintenance Véhicules',
    'version': '18.0.1.0.0',
    'category': 'Other/Others',
    'summary': 'Vehicles, intervention requests, repair orders with operations and parts, full cost per vehicle and urgency alerts',
    'description': """
Atelier & Maintenance Véhicules
===============================

Manage a vehicle fleet and its maintenance workshop: vehicles with
full history, prioritized intervention requests, repair orders with
operations (hours) and parts, complete cost calculation per order
(parts + hours x hourly rate) and per vehicle, and cron alerts on
unassigned urgent requests and overdue orders.

Key Features:
-------------
* Vehicle fleet with history of repair orders
* Prioritized intervention requests (low/normal/high/urgent)
* Repair orders: draft -> planned -> in_progress -> done -> closed
* Operations and parts per order with status tracking
* Complete order cost: parts total + hours x workshop hourly rate
* Per-vehicle cost report and printable repair order
* Cron alerts on unassigned urgent requests and overdue orders
* Multi-company with manager-restricted actions
* Configurable alert delay and hourly rate in settings

Ideal for:
* Garage and workshop mechanics
* Fleet managers and transport teams
* Company directions tracking vehicle costs
""",
    'author': 'Ethan Miller',
    'website': '',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_vehicle_workshop_security.xml',
        'security/ir.model.access.csv',
        'views/workshop_views.xml',
        'views/res_config_settings_views.xml',
        'views/workshop_menus.xml',
        'views/workshop_reports.xml',
        'data/actions.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}