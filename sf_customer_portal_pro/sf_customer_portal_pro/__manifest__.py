{
    'name': 'Customer Self-Service Portal Pro',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'B2B/B2C portal: invoices, payments, subscriptions, returns, tickets, documents',
    'description': """Customer Self-Service Portal Pro
=================================

Complete branded portal for B2B & B2C.

Features:
- Secure login (OAuth2, SAML, email+password, magic link)
- Dashboard: open invoices, order status, subscription usage, ticket summary
- Invoice payment: Stripe, Adyen, PayPal, bank transfer (auto-reconciliation)
- Subscription management: upgrade/downgrade/cancel, usage meters, payment methods
- Return/RMA initiation with label printing
- Support tickets: create, track, chat, knowledge base
- Document center: contracts, certificates, compliance docs
- Account management: users, roles, permissions, billing contacts
- White-label: custom domain, CSS, email templates
- API headless mode for custom frontend (React/Vue/Flutter)
- Multi-company, multi-lang, multi-currency

B2B specific:
- Company hierarchy (parent/child accounts)
- Purchase order submission
- Credit limit visibility
- Bulk order upload (CSV/EDI)""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 74.75,
    'currency': 'EUR',
    'depends': ['base', 'website', 'sale', 'account', 'portal', 'payment'],
    'data': [
        'security/ir.model.access.csv',
        'views/portal_menus.xml',

        'data/portal_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}


