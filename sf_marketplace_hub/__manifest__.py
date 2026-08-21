{
    'name': 'Marketplace Hub',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Multi-vendor marketplace: channels, vendors, listings and orders in one hub',
    'description': """
Marketplace Hub
===============

Run your own multi-vendor marketplace on top of Odoo.

Key Features:
-------------
* Marketplace record per channel (web store, Amazon, eBay, local)
* Vendors with commission rates and payout accounts
* Product listings managed per marketplace vendor
* Orders funneled from any channel into a single hub
* Commission computed automatically on paid amounts
* Payout batches with draft -> paid workflow
* Dashboards: GMV, commissions, vendor performance
* Multi-currency support and per-company isolation

Ideal for:
* E-commerce managers running multi-vendor platforms
* Companies aggregating sales from several channels
* Marketplaces wanting automated commission handling
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'account', 'product'],
    'data': [
        'security/marketplace_security.xml',
        'security/ir.model.access.csv',
        'data/marketplace_data.xml',
        'views/marketplace_menus.xml',
        'views/marketplace_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
