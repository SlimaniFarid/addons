{
    'name': 'Customer Rebates & Turnover Bonuses',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Sell-side rebate deals (retro %, turnover bonus, per unit) with accrual from invoices and credit note settlement',
    'description': """
Customer Rebates
================

Reward loyal customers, control the cost.

Features:
---------
* Rebate deals per customer and period: retro %, turnover bonus
  above threshold, fixed per unit; product category scope
* Monthly accrual computed from posted customer invoices
* Settlement: credit note reference and workflow
* Multi-company, currencies, chatter
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'sale', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/crebate_security.xml',
        'data/crebate_data.xml',
        'views/crebate_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
