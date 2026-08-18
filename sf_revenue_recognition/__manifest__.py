{
    'name': 'Revenue Recognition & Subscription Billing',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'ASC 606 / IFRS 15 compliant revenue recognition for subscriptions and contracts',
    'description': """Revenue Recognition & Subscription Billing
==========================================

Full ASC 606 / IFRS 15 compliance for Odoo.

Features:
- Identify performance obligations in contracts (products, services, support, training)
- Determine standalone selling prices (SSP) with observable inputs
- Allocate transaction price to obligations
- Recognize revenue over time or at point in time
- Automated deferral schedules with POC (percentage of completion)
- Contract modifications handling (variable consideration, renewals, upsells)
- Disclosure reports: contract assets/liabilities, remaining performance obligations
- Audit trail with journal entry linkage
- Multi-currency, multi-company

Use cases:
- SaaS subscriptions with setup fees, support, training
- Professional services with milestones
- Hardware + warranty + support bundles
- Construction / long-term projects""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 399.0,
    'currency': 'EUR',
    'depends': ['base', 'account', 'sale', 'account_asset'],
    'data': [
        'security/ir.model.access.csv',
        'views/revrec_menus.xml',

        'data/revrec_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}


