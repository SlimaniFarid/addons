{
    'name': 'Real Estate Property Manager',
    'version': '18.0.1.0',
    'category': 'Sales',
    'summary': 'Properties, leases, tenants and rent invoicing in one place',
    'description': """
Real Estate Property Manager
============================

Manage your property portfolio and leases in Odoo.

Key Features:
-------------
* Property records: type, surface, value, location, owner
* Leases with start/end dates, rent and deposit
* Tenant (partner) linking and payment tracking
* Automatic rent invoice generation from leases
* Property status workflow (available, rented, maintenance)
* Dashboards: portfolio value, rent income, occupancy
* Works with native Odoo invoicing

Ideal for:
* Property managers and landlords
* Real estate agencies
* Facility managers tracking spaces
* Investors monitoring portfolio income
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/real_estate_security.xml',
        'security/ir.model.access.csv',
        'data/real_estate_data.xml',
        'views/real_estate_menus.xml',
        'views/real_estate_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}