{
    'name': 'Facility & Space Management',
    'version': '18.0.1.0.0',
    'category': 'Operations/Operations',
    'summary': 'Sites, rooms and bookings with capacity control and conflict detection',
    'description': """
Facility and Space Management
=============================

Every desk, room and site under control.

Features:
---------
* Sites: address, surface, lease reference
* Rooms per site: type (office, meeting, storage), capacity, floor
* Bookings with datetime ranges and conflict detection
* Multi-company, chatter on sites
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/fac_security.xml',
        'data/fac_data.xml',
        'views/fac_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
