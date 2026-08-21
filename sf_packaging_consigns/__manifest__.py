# -*- coding: utf-8 -*-
{
    'name': 'Packaging Consigns Management',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Returnable packaging consigns: deposit types, parks per site, emissions/returns linked to deliveries, invoiced deposits, return rate and stock alerts',
    'description': """
Packaging Consigns Management
=============================

Manage returnable packaging (bottles, crates, pallets, kegs) and
their consigns for distributors, breweries and producers: deposit
packaging types (deposit amount, conditioning), parks per site,
emission and return movements linked to deliveries, invoiced
consigns (quantity x deposit amount), computed return rate, alerts
when a park falls below the minimum stock and PDF follow-up reports.

Key Features:
-------------
* Deposit packaging types (deposit amount, units per lot)
* Parks per site with computed available quantity
* Emissions and returns linked to deliveries (reference)
* Invoiced consigns via deposit_total computation
* Return rate computed per park (returns / emissions)
* Daily cron alerts when a park is below the minimum stock
* Consignment follow-up and parks status PDF reports
* Multi-company record rules and dedicated user / manager groups

Ideal for:
* Logistics and warehouse teams
* Sales and accounting departments
* Distribution, brewery and production companies
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/packaging_security.xml',
        'security/ir.model.access.csv',
        'views/packaging_views.xml',
        'views/res_config_settings_views.xml',
        'views/packaging_reports.xml',
        'views/packaging_menus.xml',
        'data/packaging_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}