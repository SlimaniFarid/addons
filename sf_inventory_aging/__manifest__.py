{
    'name': 'Inventory Aging & Obsolescence Provisions',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Stock aging buckets from last movement, slow-mover detection and obsolescence provision suggestions',
    'description': """
Inventory Aging and Obsolescence
================================

Find the dust-collecting stock before the auditors do.

Features:
---------
* Aging runs per warehouse and as-of date: days since last stock
  movement per product
* Aging buckets: 0-30, 31-90, 91-180, 180+ days with stock value
* Slow-mover and dead-stock flagging
* Provision % suggestion per bucket (configurable) and provision
  amount computation
* Multi-company, currencies, pivot analysis
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.25,
    'currency': 'EUR',
    'depends': ['base', 'stock', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/aging_security.xml',
        'data/aging_data.xml',
        'views/aging_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
