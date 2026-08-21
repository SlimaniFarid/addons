{
    'name': 'B2B Price & Discount Matrix',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Tiered pricing and discount matrix per customer category',
    'description': """
B2B Price & Discount Matrix
===========================

Tiered B2B pricing and discount rules in Odoo.

Key Features:
-------------
* Customer categories with discount levels
* Tiered pricing by quantity
* Automatic discount application on sale orders
* Price lists built from the matrix
* Override rules per customer
* Margin safety checks

Ideal for:
* Wholesale distributors
* B2B manufacturers with volume pricing
* Sales teams with category-based discounts
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'product', 'account'],
    'data': [
        'security/price_matrix_security.xml',
        'security/ir.model.access.csv',
        'data/price_matrix_data.xml',
        'views/price_matrix_menus.xml',
        'views/price_matrix_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
