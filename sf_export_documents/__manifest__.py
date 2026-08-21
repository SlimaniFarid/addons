# -*- coding: utf-8 -*-
{
    'name': 'Export Documents & Customs Compliance',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Export pack documents, Incoterms, completeness control and dossier workflow',
    'description': """
Export Documents & Customs Compliance
=====================================

Manage export dossiers: generate the export document pack
(commercial invoice, packing list, certificate of origin,
EUR.1 / ATR), manage Incoterms, ports and countries of origin,
check completeness before shipment and archive the history.

Key Features:
------------
* Export dossier workflow: draft → in_preparation → ready → shipped → archived
* Incoterms reference and transport modes
* Commercial invoice and packing list from the sale order
* Certificate of origin and EUR.1 / ATR reports
* Completeness control before shipment (4 documents)
* Overdue preparation alerts via cron
* Dashboard of dossiers by state and destination

Ideal for:
* Export departments and sales administration
* International logistics
* SMEs exporting goods
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 52.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts', 'sale', 'product'],
    'data': [
        'security/export_security.xml',
        'security/ir.model.access.csv',
        'views/export_views.xml',
        'views/export_reports.xml',
        'views/res_config_settings_views.xml',
        'views/export_menus.xml',
        'data/export_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}