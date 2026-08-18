{
    'name': 'Credit & Debt Collection',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Aging analysis, collection cases, dunning plans and payment promises',
    'description': """
Credit & Debt Collection
========================

Recover what you are owed, politely and systematically.

Key Features:
-------------
* Partner credit limits with usage tracking
* Automatic aging analysis by maturity date (current, 30, 60, 90+ days)
* Collection cases per customer with assigned collector and priority
* Dunning plan: automatic escalation levels and reminder due dates
* Payment promises with follow-up dates
* Overdue warnings and follow-up tasks
* Collection actions history (calls, emails, letters)
* Per-collector workload and performance dashboards
* Works with native Odoo accounting data

Perfect for:
* Finance and credit management teams
* SMEs that sell on credit and want to reduce late payments
* Companies wanting a clear, professional dunning process

Install, open the Collections menu, and start recovering your cash.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/debt_security.xml',
        'security/ir.model.access.csv',
        'data/debt_data.xml',
        'views/debt_menus.xml',
        'views/debt_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}