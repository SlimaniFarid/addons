# -*- coding: utf-8 -*-
{
    'name': 'Field Sales Routes & Territory Management',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Plan field sales routes, track visits, territories and objectives',
    'description': """
Field Sales Routes & Territory Management
==========================================

Plan and track field sales activities: territories, routes,
visits with check-in/check-out, orders and objectives.

Key Features:
-------------
* Territory management with customer assignment
* Route planning with ordered visits
* Visit check-in / check-out with timestamps
* Visit results (order, opportunity, information)
* Order and opportunity creation from a visit
* Objectives per territory and period
* Performance dashboard for field sales

Ideal for:
* Distribution and FMCG sales teams
* Pharmacy and medical reps
* Field service and door-to-door sales
* Sales managers and commercial directors
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 52.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'crm'],
    'data': [
        'security/routes_security.xml',
        'security/ir.model.access.csv',
        'views/routes_menus.xml',
        'views/routes_views.xml',
        'data/routes_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
