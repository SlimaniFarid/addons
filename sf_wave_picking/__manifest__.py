{
    'name': 'Warehouse Wave Picking',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Group pickings into waves and release them efficiently',
    'description': """
Warehouse Wave Picking
======================

Group pickings into waves and release them efficiently.

Key Features:
-------------
* Waves grouping pickings by warehouse and picking type
* Automatic wave creation from a selection of pickings
* Release waves in one click
* Validate all pickings of a wave together
* Progress tracking per wave
* Integration with native batch picking

Ideal for:
* E-commerce and distribution warehouses
* High-volume picking operations
* Teams picking in batches
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'stock', 'stock_picking_batch', 'mail'],
    'data': [
        'security/wave_picking_security.xml',
        'security/ir.model.access.csv',
        'views/wave_picking_menus.xml',
        'views/wave_picking_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
