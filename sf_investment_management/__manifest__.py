# -*- coding: utf-8 -*-
{
    'name': 'Investment Management & Portfolios',
    'version': '18.0.1.0',
    'category': 'Finance',
    'summary': 'Portfolios, investment lines, valuations, dividends and coupons, maturity alerts and PDF performance reports',
    'description': """
Investment Management & Portfolios
===================================

Manage investment portfolios and lines (stocks, bonds, money market
and term deposits), market-price valuations by date, dividends and
coupon receipts with computed revenues, maturity alerts for bonds and
term deposits, and PDF performance reports per portfolio.

Key Features:
-------------
* Portfolios per company account, bank and responsible
* Investment lines with security type, ISIN, quantity and prices
* Computed line value and latent gain/loss
* Valuation history by market price and date
* Dividend and coupon incomes with computed amounts
* Daily maturity alerts (activity deduplicated)
* PDF performance and maturity reports
* Multi-company security groups and record rules

Ideal for:
* Treasury / finance teams
* CFO and management
* Investment committees
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/invest_security.xml',
        'security/ir.model.access.csv',
        'views/invest_views.xml',
        'views/res_config_settings_views.xml',
        'views/invest_menus.xml',
        'views/invest_reports.xml',
        'data/invest_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}