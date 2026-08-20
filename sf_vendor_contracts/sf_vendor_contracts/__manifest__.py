{
    'name': 'Supplier Contract & Agreement Manager',
    'version': '18.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Manage supplier contracts, clauses, amounts, expirations and renewals with alerts',
    'description': """
Supplier Contract & Agreement Manager
=====================================

Centralize your supplier contracts with clauses, amounts,
expiration dates and automatic renewal alerts.

Key Features:
-------------
* Supplier contract register
* Contract types, amounts and currencies
* Clauses and product lines
* Expiration and renewal alerts (activities)
* Contract versions and renewal history
* Expiring contracts report
* Contract register report

Ideal for:
* Procurement teams tracking supplier agreements
* Legal teams checking clauses and renewals
* Finance teams reviewing financial commitments
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 47.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'product', 'mail'],
    'data': [
        'data/vendor_contract_data.xml',
        'data/vendor_contract_cron.xml',
        'security/vendor_contract_security.xml',
        'security/ir.model.access.csv',
        'views/vendor_contract_menus.xml',
        'views/vendor_contract_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}