# -*- coding: utf-8 -*-
{
    'name': 'Gym & Fitness Management',
    'summary': 'Gym memberships, plans, group classes, sessions, attendances and payments with automatic alerts',
    'description': """
Gym & Fitness Management
========================

Manage gym members and their sports subscriptions, membership plans
with monthly prices, group lessons with maximum capacity, session
planning with coaches, member attendances and membership payments.

Key Features:
------------
* Members with contact details, birth date and photo
* Membership plans with monthly price and duration
* Group lessons with maximum capacity per session
* Session planning with coaches and attendance tracking
* Subscription payments and automatic paid status
* Automatic alerts for expiring subscriptions and empty sessions (cron)
* PDF reports: subscription contract and session planning
* Per-company access rules

Ideal for:
* Fitness clubs and gyms
* Coaches and front desk teams
* Gym managers
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': '',
    'category': 'Other/Others',
    'version': '19.0.1.0.0',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'application': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_gym_fitness_security.xml',
        'security/ir.model.access.csv',
        'views/sf_gym_fitness_views.xml',
        'views/sf_gym_fitness_reports.xml',
        'views/res_config_settings_views.xml',
        'views/sf_gym_fitness_menus.xml',
        'data/actions.xml',
    ],
    'installable': True,
    'auto_install': False,
}

