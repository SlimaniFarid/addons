# -*- coding: utf-8 -*-
{
    'name': 'Occupational Health & Medical Surveillance',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Medical visits, aptitudes, restrictions, vaccinations and compliance dashboard',
    'description': """
Occupational Health & Medical Surveillance
===========================================

Track mandatory medical visits (hire, periodic, return to work),
periodicities by job and exposure, doctors and practices,
aptitude results (fit / fit with restrictions / unfit), validity
dates and renewal alerts, vaccinations and job restrictions, and
a compliance dashboard by site. Integrated with employees (hr).

Key Features:
-------------
* Per-employee medical surveillance files
* Medical visits: planning, scheduling, results, validity
* Exposure reasons with default periodicities
* Expiry alerts via daily cron (configurable threshold)
* Job restrictions and contraindications
* Vaccination records
* Compliance dashboard and next due dates

Ideal for:
* HR / occupational health managers
* Occupational doctors and practices
* QHSE teams and plant managers
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 57.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/oh_security.xml',
        'security/ir.model.access.csv',
        'views/oh_views.xml',
        'views/hr_employee_views.xml',
        'views/res_config_settings_views.xml',
        'views/oh_menus.xml',
        'data/oh_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
