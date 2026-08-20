# -*- coding: utf-8 -*-
{
    'name': 'ESG Reporting (CSRD)',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Collect, validate and report ESG indicators (environment, social, governance) per company and period for CSRD compliance',
    'description': """
ESG Reporting (CSRD)
====================

Collect and report ESG indicators for CSRD compliance: configurable
indicator repository (environment / social / governance), period-based
collection per company with targets, automatic variation and target
achievement computation at validation time, regulatory PDF report and
CSV export.

Key Features:
-------------
* Configurable ESG indicator repository (category, unit, direction, frequency)
* Periods with a validation workflow (draft -> submitted -> approved -> closed)
* Values per company and period with target and variation
* Automatic variation (previous period) and target achievement (value/target)
* ESG PDF report per company and period
* CSV export of collected values
* Dashboard of values by indicator category

Ideal for:
* Sustainability / RSE teams
* Finance and management control (validation)
* Top management (read-only reporting)
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/esg_security.xml',
        'security/ir.model.access.csv',
        'views/esg_views.xml',
        'views/res_config_settings_views.xml',
        'views/esg_reports.xml',
        'views/esg_menus.xml',
        'data/esg_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}