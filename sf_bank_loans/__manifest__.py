# -*- coding: utf-8 -*-
{
    'name': 'Bank Loans & Credits',
    'version': '18.0.1.0',
    'category': 'Accounting',
    'summary': 'Track bank loans, calculated amortization schedules, drawdowns, early repayments and covenants with alerts',
    'description': """
Bank Loans & Credits
====================

Track bank financing: loan files (bank, amount, rate, term),
calculated amortization schedules (annuity or constant), drawdowns
and early repayments, covenants with breach alerts, debt
projection and a debt position report by bank.

Key Features:
-------------
* Banks and contacts
* Loan files with workflow (draft → offered → disbursing →
  active → closed)
* Amortization schedule generation (annuity or constant)
* Drawdowns that update the disbursed capital
* Early repayments that adjust the remaining debt
* Covenants with target range and breach alerts
* Daily cron that alerts breached covenants and overdue installments
* Debt position report by bank and amortization schedule PDF
* Debt dashboard

Ideal for:
* Treasury / finance teams
* CFO (DAF)
* General management
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/loan_security.xml',
        'security/ir.model.access.csv',
        'data/loan_data.xml',
        'views/loan_views.xml',
        'views/loan_reports.xml',
        'views/res_config_settings_views.xml',
        'views/loan_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}