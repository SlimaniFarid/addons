{
    'name': 'Vendor Portal & e-Procurement',
    'version': '18.0.1.0.0',
    'category': 'Purchasing',
    'summary': 'Self-service vendor portal: RFQs, quotations, orders and invoices online',
    'description': """
Vendor Portal & e-Procurement
=============================

Let your suppliers collaborate online instead of exchanging emails.

Key Features:
-------------
* Secure self-service portal for each vendor (portal access)
* Vendors see their quotations (RFQs), confirmed orders and invoices
* RFQ / quotation flow: vendor can accept, decline or propose a counter-offer
* Confirmed orders visible with lines, prices and dates
* Invoices and payments tracked for the vendor
* Portal summary page per vendor with amounts and statuses
* Automatic welcome message with secure portal link
* Optional approval before quotations become orders

Perfect for:
* Purchasing departments wanting to streamline RFQs
* Companies moving away from email-based procurement
* Vendors wanting self-service access to their documents

Works with native Odoo purchase and portal modules.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 99.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'purchase', 'portal', 'account', 'mail'],
    'data': [
        'security/vendor_portal_security.xml',
        'security/ir.model.access.csv',
        'data/vendor_portal_data.xml',
        'views/vendor_portal_menus.xml',
        'views/vendor_portal_views.xml',
        'views/vendor_portal_templates.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}