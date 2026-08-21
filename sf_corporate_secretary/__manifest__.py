# -*- coding: utf-8 -*-
{
    'name': 'Corporate Secretary & Corporate Life',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Corporate secretariat: organs, AG/board meetings, convocations, resolutions, votes, minutes, written decisions and regulatory deadlines',
    'description': """
Corporate Secretary & Corporate Life
====================================

Manage the corporate life of the company: organs (general
meetings, board of directors), convocations and tracked sending,
assemblies with resolutions and votes, proxies, minutes (PV),
written decisions (simplified procedure), representatives and
mandates, and the regulatory deadlines agenda per company.

Key Features:
-------------
* Organ registry (AGA, AGE, board, supervisory board) with
  chairperson, members and notice periods
* Assembly workflow: planned -> in progress -> done -> archived
* Convocation workflow: draft -> sent -> held -> minutes done
* Resolutions with votes and automatic adoption rule
* Meeting minutes (PV) PDF report with votes and adoption
* Written decisions: draft -> signed -> filed
* Regulatory formality schedule with PDF report
* Daily cron generating activities for upcoming deadlines
* Multi-company record rules and manager-only closures

Ideal for:
* Corporate secretaries and legal teams
* Company secretariats and notaries
* Directors and presidents (read access)
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/corporate_security.xml',
        'security/ir.model.access.csv',
        'views/corporate_views.xml',
        'views/corporate_reports.xml',
        'views/res_config_settings_views.xml',
        'views/corporate_menus.xml',
        'data/corporate_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
