{
    'name': 'Tool & Gauge Management',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Manufacturing',
    'summary': 'Track tools, gauges, fixtures with calibration, wear, and lifecycle',
    'description': """
Tool & Gauge Management
=======================

Complete lifecycle management for tools, gauges, and fixtures.

Key Features:
-------------
* Tool registry with specifications and classifications
* Calibration scheduling and certificate management
* Wear tracking with replacement alerts
* Tool assignment to workcenters and operations
* Check-in/check-out with operator accountability
* Cost tracking and depreciation
* Integration with maintenance and quality

Ideal for:
* Machine shops and precision manufacturing
* Aerospace and automotive suppliers
* Tool rooms and metrology labs
* Any production using calibrated tools
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mrp', 'stock', 'maintenance', 'quality'],
    'data': [
        'security/tool_management_security.xml',
        'security/ir.model.access.csv',
        'views/tool_management_menus.xml',
        'views/tool_management_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
