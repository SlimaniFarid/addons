{
    'name': 'Andon & Alert System',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Real-time Andon alerts, escalation and response tracking for shop floor',
    'description': """
Andon & Alert System
====================

Real-time visual management for manufacturing shop floor.

Key Features:
-------------
* Andon calls (quality, maintenance, material, safety)
* Multi-level escalation with SLA
* Visual boards (tower lights, screens, mobile)
* Response tracking and acknowledgment
* Downtime reason categorization
* Analytics: MTTR, alert frequency, response times
* Integration with MES work orders and maintenance

Ideal for:
* Lean manufacturing environments
* Automotive, electronics, discrete manufacturing
* Plants using Andon cords/buttons/towers
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mrp', 'stock', 'maintenance', 'mail'],
    'data': [
        'security/mes_andons_security.xml',
        'security/ir.model.access.csv',
        'data/mes_andons_data.xml',
        'views/mes_andons_menus.xml',
        'views/mes_andons_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}