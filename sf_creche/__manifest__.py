# -*- coding: utf-8 -*-
{
    'name': 'Creche Management',
    'summary': 'Children, enrollments, daily attendance, room capacity control and monthly hourly billing',
    'description': """
Creche Management
=================

Centralize children records, enrollments with schedules, daily
attendance with arrival/departure times, rooms with capacity
control (educator/child ratio verified) and monthly billing
computed on real attended hours.

Key Features:
-------------
* Children records (identity, birth date, parents, allergies)
* Enrollments with schedule (full time / half day)
* Daily attendance with arrival and departure times
* Room capacity check at attendance close (capacity limit)
* Monthly billing based on real hours x hourly rate
* End-date reminder alerts via cron (deduplicated activities)
* PDF monthly invoice and attendance register reports
* Multi-company record rules and manager workflow

Ideal for:
* Creches and daycares
* Educators and administrative staff
* Directors checking headcounts and ratios
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': '',
    'category': 'Other/Others',
    'version': '19.0.1.0.0',
    'license': 'OPL-1',
    'price': 62.50,
    'application': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_creche_security.xml',
        'security/ir.model.access.csv',
        'views/sf_creche_views.xml',
        'views/sf_creche_menus.xml',
        'views/res_config_settings_views.xml',
        'views/sf_creche_reports.xml',
        'data/creche_data.xml',
        'data/actions.xml',
    ],
    'installable': True,
    'auto_install': False,
}

