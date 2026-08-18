{
    'name': 'Sales Commission Engine',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Flexible commission plans, auto-computed from paid invoices and tracked per salesperson',
    'description': """
Sales Commission Engine
=======================

Compute and manage sales commissions automatically, with flexible and
transparent rules that your sales team will understand.

Key Features:
-------------
* Commission plans with flat, tiered and percentage-of-margin rates
* Commission per product category override (higher rates on strategic products)
* Based on the paid invoice amount (commission earned when the customer pays)
* Automatic commission line generation from validated invoices and payments
* Manual adjustments: prorated commissions, fixed bonuses, clawbacks
* Commission per salesperson, with amounts in the company currency
* Draft / Approved / Paid / Cancelled workflow
* Approval workflow: manager validates before payment
* Totals per period and per salesperson
* Dedicated menus and reporting views

Perfect for:
* Sales teams and sales managers
* SMEs wanting a transparent, data-driven incentive scheme
* Companies replacing spreadsheet-based commission calculations

No code required: define plans and rates from the UI, then let Odoo compute.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 99.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'account'],
    'data': [
        'security/commission_security.xml',
        'security/ir.model.access.csv',
        'views/commission_views.xml',
        'views/sale_order_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}