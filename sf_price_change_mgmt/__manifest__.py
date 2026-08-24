{
    'name': 'Price Change Management',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Plan, announce and apply price increases: product lines with old/new price, delta %, effective dates and one-click application',
    'description': """
Price Change Management
=======================

Raise prices in a controlled, documented way.

Features:
---------
* Price change campaigns: announcement date, effective date, reason
* Lines per product: old price, new price, computed delta %
* One-click application to product list prices at effective date
* Cancel before effective date, full audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.00,
    'currency': 'EUR',
    'depends': ['base', 'product', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/pc_security.xml',
        'data/pc_data.xml',
        'views/pc_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
