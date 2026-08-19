{
    'name': 'IT Asset & License Manager',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Track IT equipment, software licenses, assignments and warranties',
    'description': """
IT Asset & License Manager
==========================

Centralize your IT fleet: equipment, software licenses,
assignments, warranties and maintenance.

Key Features:
-------------
* Equipment inventory with categories and states
* Employee assignment tracking
* Software license management with seats and expiration
* Warranty and license expiry alerts
* Valued inventory report
* License compliance report

Ideal for:
* IT departments managing hardware fleets
* Finance teams tracking inventory value
* Companies needing license compliance
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 47.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr'],
    'data': [
        'data/it_asset_data.xml',
        'data/it_asset_cron.xml',
        'security/it_asset_security.xml',
        'security/ir.model.access.csv',
        'views/it_asset_menus.xml',
        'views/it_asset_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}