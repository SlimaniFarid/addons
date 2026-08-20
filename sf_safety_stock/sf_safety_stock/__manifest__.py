{
    'name': 'Safety Stock Optimizer',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Optimal safety stock levels and reorder points from real demand',
    'description': """
Safety Stock Optimizer
======================

Compute and maintain optimal safety stock and reorder points in Odoo.

Key Features:
-------------
* Safety stock computed from real historical demand
* Reorder point per product and warehouse
* Suggested order quantity on reorder
* Service level selection (90%, 95%, 99%)
* Alerts for products at or below reorder point
* Demand analysis window configurable per product

Ideal for:
* Warehouse managers tuning stock levels
* Supply planners preventing stockouts
* E-commerce ops keeping availability high
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'stock', 'product', 'mail'],
    'data': [
        'security/safety_stock_security.xml',
        'security/ir.model.access.csv',
        'data/safety_stock_data.xml',
        'views/safety_stock_menus.xml',
        'views/safety_stock_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}