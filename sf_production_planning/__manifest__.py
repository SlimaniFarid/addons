# -*- coding: utf-8 -*-
{
    'name': 'Production Master Scheduling (MPS)',
    'version': '18.0.1.0',
    'category': 'Manufacturing',
    'summary': 'Master production schedule with Gantt, priorities and work center load',
    'description': """
Production Master Scheduling (MPS)
==================================

Plan production by work center and period, schedule manufacturing
orders with priorities, visualize the schedule in a Gantt view and
monitor the load per work center.

Key Features:
------------
* Master production plans over a period with workflow
* Plan lines per work center, product and dates
* Load manufacturing orders (MRP) into the plan
* Gantt scheduling view colored by priority
* Work center load calculation
* Plan confirmation and closure

Ideal for:
* Production planners and schedulers
* Industrial directors and workshop managers
* SME manufacturers
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 55.00,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'mrp'],
    'data': [
        'security/production_security.xml',
        'security/ir.model.access.csv',
        'views/production_views.xml',
        'views/production_reports.xml',
        'views/res_config_settings_views.xml',
        'views/production_menus.xml',
        'data/production_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}