{
    'name': 'Shop Floor Execution (MES)',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Track work orders, stations, downtime and quality on the floor',
    'description': """
Shop Floor Execution (MES)
==========================

Bring live execution to the shop floor.

Key Features:
-------------
* Station registry with workcenters
* Shop floor work orders with lifecycle
* Operator assignment and logging
* Downtime tracking with reasons
* Inline quality checks per order
* Real-time production progress

Ideal for:
* Manufacturers and assemblers
* Machine shops and jobbing
* Teams running Odoo Manufacturing
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mrp', 'stock', 'quality'],
    'data': [
        'security/mes_shop_floor_security.xml',
        'security/ir.model.access.csv',
        'views/mes_shop_floor_menus.xml',
        'views/mes_shop_floor_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
