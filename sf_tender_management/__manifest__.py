# -*- coding: utf-8 -*-
{
    'name': 'Tender Management & Sourcing (RFx)',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Manage RFQ/RFI/RFP and public tenders with criteria scoring and justified award',
    'description': """
Tender Management & Sourcing (RFx)
==================================

Manage the full lifecycle of a tender / procurement consultation
(RFQ, RFI, RFP, public tender): published dossier, dated supplier
offers, weighted multi-criteria evaluation matrix, automatic
scoring, justified award decision and audit archiving.

Key Features:
------------
* Tender dossier with submission deadline and workflow
* Dated offer deposits per supplier
* Weighted evaluation criteria and automatic weighted score
* Justified award decision with mandatory reason
* Deadline alerts via cron
* Evaluation summary report and dashboard

Ideal for:
* Procurement and purchasing teams
* Contract award committees and internal audit
* Public and private sourcing processes
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 65.00,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/tender_security.xml',
        'security/ir.model.access.csv',
        'views/tender_views.xml',
        'views/tender_reports.xml',
        'views/res_config_settings_views.xml',
        'views/tender_menus.xml',
        'data/tender_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}