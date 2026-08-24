{
    'name': 'Supplier Rebates & Retro-discounts',
    'version': '18.0.1.0.0',
    'category': 'Purchase/Purchase',
    'summary': 'Vendor rebate deals (volume bonus, retro %), automatic accrual from posted bills, claims and settlement tracking',
    'description': """
Supplier Rebates and Retro-discounts
====================================

Never leave negotiated vendor money on the table.

Features:
---------
* Rebate deals per vendor and period: turnover bonus (fixed amount
  above threshold), retro percentage on purchases, or fixed rebate
  per unit
* Scope by product category
* Automatic accrual computed from posted vendor bills in the deal
  period, with progress toward threshold
* Claims: amount claimed to vendor, credit note reference,
  settlement status
* Multi-company, currencies, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 69.75,
    'currency': 'EUR',
    'depends': ['base', 'account', 'purchase', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/rebate_security.xml',
        'data/rebate_data.xml',
        'views/rebate_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
