# -*- coding: utf-8 -*-
{
    'name': 'Privacy & RGPD',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Data protection register (RGPD): treatments, processors, DPIA, breach and data subject rights management',
    'description': """
Privacy & RGPD
==============

Register of personal data processing and RGPD governance: treatments
(purposes, legal bases, retention periods, recipients), processors
and DPA contracts, impact assessments (AIPD) with risks and measures,
breach register (72 h notification deadline), data subject rights
requests and periodic review alerts with exportable proof of
compliance.

Key Features:
-------------
* Treatment register with workflow and legal basis
* Processors and DPA contracts register
* Impact assessments (AIPD) with risk score and manager validation
* Breach register with 72 h notification deadline
* Data subject rights requests management
* Periodic review alerts via cron (configurable)
* Exportable treatment and breach registers (PDF)

Ideal for:
* DPO / data protection officers
* Legal departments
* IT and security (RSSI)
* HR and marketing teams
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/privacy_security.xml',
        'security/ir.model.access.csv',
        'views/privacy_views.xml',
        'views/res_config_settings_views.xml',
        'views/privacy_reports.xml',
        'views/privacy_menus.xml',
        'data/privacy_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}