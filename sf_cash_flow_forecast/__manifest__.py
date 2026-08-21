# -*- coding: utf-8 -*-
{
    'name': 'Cash Flow & Treasury Manager',
    'version': '18.0.1.0',
    'category': 'Accounting/Accounting',
    'summary': 'Forecast cash position, track receivables/payables and avoid liquidity gaps',
    'description': """
Cash Flow & Treasury Manager
============================

Know every morning whether you can pay your suppliers this month.

Key Features:
-------------
* Rolling cash position: current bank balance plus expected inflows and outflows
* Automatic inflow forecast from open customer invoices (receivables) by due date
* Automatic outflow forecast from open vendor bills and purchase orders by due date
* Manual cash flow lines: planned payments, loans, transfers, investments
* Cash flow projection over a configurable horizon (7, 30, 60, 90, 180 days)
* Low-balance alerts and threshold warnings
* Expected balance per day, running balance per line
* Chart view (bar/line) of the projected cash position
* Group by: account, partner, category, day/week/month

Perfect for:
* CFOs, controllers and financial managers
* Small and medium businesses without treasury software
* Companies wanting to avoid overdrafts and liquidity gaps

Works with native Odoo accounting data. Install and open the Cash Flow dashboard.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'account', 'purchase'],
    'data': [
        'security/cashflow_security.xml',
        'security/ir.model.access.csv',
        'data/cashflow_data.xml',
        'views/cashflow_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}