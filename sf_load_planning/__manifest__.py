{
    'name': 'Load & Pallet Planning',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Build truck loads from pickings with capacity checks (weight, volume, pallets), route stops and load manifest',
    'description': """
Load and Pallet Planning
========================

Group deliveries into compliant truck loads before they hit the dock.

Features:
---------
* Load plans: carrier, vehicle, departure date, route stops sequence
* Assign pickings to a load; weight, volume and pallet counts computed
* Capacity limits per load with overload warnings
* Route stops with planned arrival times
* Load manifest printing, multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 229.00,
    'currency': 'EUR',
    'depends': ['base', 'stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/load_security.xml',
        'data/load_data.xml',
        'views/load_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
