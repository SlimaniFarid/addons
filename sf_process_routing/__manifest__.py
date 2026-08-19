{
    'name': 'Dynamic Process Routing',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Alternative routing selection based on conditions, capacity, and quality',
    'description': """
Dynamic Process Routing
=======================

Select the optimal production route dynamically based on real-time conditions.

Key Features:
-------------
* Multiple routing definitions per product
* Condition-based routing selection (capacity, quality, cost, lead time)
* Automatic routing selection at MO creation
* Manual override with audit trail
* Routing versioning and effectivity dates
* Cost and time comparison across routes
* Integration with workcenters and BOM

Ideal for:
* Make-to-order with multiple production paths
* Plants with flexible manufacturing cells
* Products with alternative processes
* Dynamic scheduling based on load
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mrp', 'stock'],
    'data': [
        'security/process_routing_security.xml',
        'security/ir.model.access.csv',
        'views/process_routing_menus.xml',
        'views/process_routing_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}