{
    'name': 'Product End-of-Life & Last-Time-Buy',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Phase-out planning: EOL announcements, last-time-buy dates, replacement mapping, open order checks and sale blocking',
    'description': """
Product End-of-Life Management
==============================

Retire products cleanly, keep customers served.

Features:
---------
* EOL records per product: announcement date, EOL date,
  last-time-buy date, replacement product
* Open sales order detection at phase-out
* One-click sale blocking on discontinuation
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 229.00,
    'currency': 'EUR',
    'depends': ['base', 'product', 'sale', 'stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/eol_security.xml',
        'data/eol_data.xml',
        'views/eol_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
