{
    'name': 'Service Contracts & SLA Engine',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Service contracts, SLA tiers and breach tracking',
    'description': """
Service Contracts & SLA Engine
==============================

Manage service contracts with SLA tiers in Odoo.

Key Features:
-------------
* Contracts with start/end dates and recurring billing
* SLA tiers: bronze, silver, gold with response targets
* SLA breach tracking on service tickets
* Contract status workflow: draft, active, expired, cancelled
* Automatic breach escalation
* Recurring invoice generation

Ideal for:
* IT and managed service providers
* Support teams with service level commitments
* Any business selling service plans
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'account', 'mail'],
    'data': [
        'security/service_contracts_security.xml',
        'security/ir.model.access.csv',
        'data/service_contracts_data.xml',
        'views/service_contracts_menus.xml',
        'views/service_contracts_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
