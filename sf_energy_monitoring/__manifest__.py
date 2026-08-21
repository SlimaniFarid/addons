{
    'name': 'Energy & Utility Consumption Monitoring',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Track energy and utility consumption per site and meter with ESG reporting',
    'description': """
Energy & Utility Consumption Monitoring
=======================================

Track electricity, gas and water consumption per site and
meter with cost allocation and reduction targets.

Key Features:
-------------
* Sites and meters modeling
* Periodic reading entry with confirmation
* Automatic consumption and cost calculation
* Reduction targets with breach alerts
* Dashboard and ESG reports
* CSV reading import

Ideal for:
* Facility managers tracking utility costs
* QHSE teams preparing ESG reports
* Companies reducing energy consumption
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 50.00,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail'],
    'data': [
        'data/energy_monitoring_data.xml',
        'data/energy_monitoring_cron.xml',
        'security/energy_monitoring_security.xml',
        'security/ir.model.access.csv',
        'views/energy_monitoring_menus.xml',
        'views/energy_monitoring_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
