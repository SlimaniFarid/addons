# -*- coding: utf-8 -*-
{
    'name': 'Insurance & Claims Management',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Insurance policies, premiums, guarantees, renewals and claims with indemnities',
    'description': """
Insurance & Claims Management
=============================

Centralize the company insurance program: insurers, policies with
guarantees, premiums and maturities, automatic renewals, claims with
declaration and follow-up up to indemnification, risk evaluation and
a dashboard of the whole insurance program per company.

Key Features:
-------------
* Insurers and intermediaries reference (partner linked)
* Policies: type, guarantees, premium, dates, status and renewal
* Automatic policy expiry and renewal via cron
* Claims: declaration, status, estimation and settlement / rejection
* Settlement amount control (warning when above the estimation)
* Renewal and declaration reminder activities (configurable delay)
* Insurance Program and Claims Report PDF
* Dashboard by policy type and status

Ideal for:
* Insurance managers and risk managers
* Finance departments
* Legal departments
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/insurance_security.xml',
        'security/ir.model.access.csv',
        'views/insurance_views.xml',
        'views/insurance_reports.xml',
        'views/res_config_settings_views.xml',
        'views/insurance_menus.xml',
        'data/insurance_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

