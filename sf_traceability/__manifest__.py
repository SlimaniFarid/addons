{
    'name': 'Traceability & Batch Recall',
    'version': '18.0.1.0',
    'category': 'Inventory',
    'summary': 'Full batch traceability, recall events and product history',
    'description': """
Traceability & Batch Recall
===========================

Full traceability for batches and serial numbers in Odoo.

Key Features:
-------------
* Batch recall events with severity levels
* Affected customers computed from deliveries
* Full product movement history per lot
* Recall workflow: open, in progress, closed
* Notifications to affected partners
* Batch quality status tracking

Ideal for:
* Food and beverage manufacturers
* Pharmaceutical and cosmetics industries
* Any business required to recall batches
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'stock', 'product', 'mail'],
    'data': [
        'security/traceability_security.xml',
        'security/ir.model.access.csv',
        'data/traceability_data.xml',
        'views/traceability_menus.xml',
        'views/traceability_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}