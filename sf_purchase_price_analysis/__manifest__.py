{
    'name': 'Purchase Price Variance & Cost Analysis',
    'version': '18.0.1.0.0',
    'category': 'Purchase/Purchase',
    'summary': 'PPV per product/vendor vs standard cost from posted bills, price change history and increase alerts',
    'description': """
Purchase Price Variance Analysis
================================

See exactly where purchase prices drift from standard.

Features:
---------
* Analysis runs per period: actual average purchase price per
  product/vendor computed from posted vendor bills
* Variance vs standard cost: amount and %, threshold flagging
* Price change history per product/vendor across periods
* Increase alerts beyond tolerance %
* Vendor comparison per product: who is cheapest over the window
* Multi-company, currencies, pivot and graph views
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'purchase', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/ppv_security.xml',
        'data/ppv_data.xml',
        'views/ppv_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
