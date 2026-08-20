{
    'name': 'CPQ for Custom Products',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Configure custom products, compute prices and generate quotes',
    'description': """
CPQ for Custom Products
=======================

Configure-to-order engine for custom products in Odoo.

Key Features:
-------------
* Attribute groups with options per product
* Price adjustments computed from selected options
* Configuration records saved and reusable
* Quote generation from a configuration
* Versioned configurations per product

Ideal for:
* Manufacturers selling custom products
* Sales teams quoting configured goods
* Any business with configurable SKUs
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'product', 'mail'],
    'data': [
        'security/cpq_security.xml',
        'security/ir.model.access.csv',
        'data/cpq_data.xml',
        'views/cpq_menus.xml',
        'views/cpq_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}