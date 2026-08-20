# -*- coding: utf-8 -*-
{
    'name': 'Compliance Documents & Licenses Register',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Track licenses, permits, certifications and insurance expirations with alerts',
    'description': """
Compliance Documents & Licenses Register
=========================================

Central register for all company documents that expire:
licenses, permits, certifications, agreements and insurance.

Key Features:
-------------
* Centralized document register with types and categories
* Responsible owners per document
* Automatic expiry status (active / expiring / expired)
* Automatic renewal alerts via email and activities
* Renewal workflow with full history
* Attachments per document
* Compliance dashboard and reports

Ideal for:
* Compliance and administration teams
* Procurement (insurance, agreements)
* HR (permits, certifications)
* Maintenance (equipment and installation permits)
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 52.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail'],
    'data': [
        'security/compliance_security.xml',
        'security/ir.model.access.csv',
        'views/compliance_menus.xml',
        'views/compliance_views.xml',
        'data/compliance_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}