{
    'name': 'Freight & Carrier Costing',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Track carriers, cost formulas and freight on pickings',
    'description': """
Freight & Carrier Costing
=========================

Estimate and track freight costs per carrier and per picking.

Key Features:
-------------
* Carrier registry with cost formulas
* Cost methods: fixed, per kg, per m3, by value
* Minimum charge handling
* Automatic cost estimation on pickings
* Actual cost capture at validation
* Freight cost reports

Ideal for:
* Importers and exporters
* Distribution businesses shipping frequently
* Logistics teams tracking transport spend
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'stock', 'account'],
    'data': [
        'security/freight_costing_security.xml',
        'security/ir.model.access.csv',
        'views/freight_costing_menus.xml',
        'views/freight_costing_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}