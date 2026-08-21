# -*- coding: utf-8 -*-
{
    'name': 'Product Compliance & Technical Documentation',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Regulatory compliance of products (CE, RoHS, REACH, UL, FDA): regulations, requirements, compliance dossiers and certificates with expiry alerts',
    'description': """
Product Compliance & Technical Documentation
============================================

Regulatory compliance of products (CE, RoHS, REACH, UL, FDA):
regulations reference, requirements per product, compliance
dossiers with documents and validations, certificates with
expiry dates and alerts, compliance status by market and
import of declarations of conformity.

Key Features:
-------------
* Regulation / market reference (CE, RoHS, REACH, UL, FDA)
* Product requirements with evidence and satisfaction tracking
* Compliance dossiers with validation workflow and attachments
* Certificates with expiry dates and automatic alerts (cron)
* Computed product compliance status per regulation
* PDF compliance report and expired certificates list
* Dashboard of dossiers by state and regulation

Ideal for:
* Compliance officers and regulatory affairs
* R&D / engineering teams
* Quality departments
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'product', 'contacts'],
    'data': [
        'security/compliance_security.xml',
        'security/ir.model.access.csv',
        'views/compliance_views.xml',
        'views/compliance_menus.xml',
        'views/res_config_settings_views.xml',
        'views/compliance_reports.xml',
        'data/compliance_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
