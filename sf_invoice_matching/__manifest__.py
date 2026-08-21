# -*- coding: utf-8 -*-
{
    'name': 'Automated Supplier Invoice Control (3-Way Match)',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Automatic purchase order / receipt / invoice reconciliation with tolerances and exceptions',
    'description': """
Automated Supplier Invoice Control (3-Way Match)
=================================================

Compare invoices against purchase orders and receipts
automatically: quantity, unit price, taxes and discounts, with
configurable tolerances (amount / %) and a full exception
workflow. Payment stays blocked until major discrepancies are
resolved.

Key Features:
-------------
* Automatic 3-way comparison: order, receipt, invoice
* Configurable tolerances per company and per supplier
* Statuses: matched / minor / major discrepancy
* Exception workflow with responsible and decisions
* Payment and validation blocked while a major exception is open
* Full match history and discrepancy dashboard by supplier

Ideal for:
* Accounts payable teams
* Financial controllers and AP managers
* Buyers resolving price and quantity differences
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'purchase', 'purchase_stock', 'account',
                'mail'],
    'data': [
        'security/match_security.xml',
        'security/ir.model.access.csv',
        'views/match_views.xml',
        'views/account_move_views.xml',
        'views/res_config_settings_views.xml',
        'views/match_menus.xml',
        'data/match_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
