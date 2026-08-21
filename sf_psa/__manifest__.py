{
    'name': 'Professional Services Automation',
    'version': '18.0.1.0',
    'category': 'Services/Project',
    'summary': 'Manage engagements, resources and time for services teams',
    'description': """
Professional Services Automation
=================================

Run a professional services business in Odoo.

Key Features:
-------------
* Client engagements with budgets
* Resource pool with roles and rates
* Assignments with allocation and billing rates
* Time entries linked to engagements
* Utilisation and progress reporting
* Automated invoice-ready data

Ideal for:
* Consulting firms
* Agencies and studios
* Managed services providers
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'project', 'hr', 'account', 'mail'],
    'data': [
        'security/psa_security.xml',
        'security/ir.model.access.csv',
        'views/psa_menus.xml',
        'views/psa_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}