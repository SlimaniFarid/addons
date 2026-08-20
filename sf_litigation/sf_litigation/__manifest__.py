# -*- coding: utf-8 -*-
{
    'name': 'Litigation & Legal Case Management',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Legal cases and pre-litigation: cases and parties, domains, procedural deadlines with alerts, fees and honoraries, decisions and results, legal activity PDF report',
    'description': """
Litigation & Legal Case Management
==================================

Manage legal matters and pre-litigation: cases and parties
(plaintiff, defendant, third parties), legal domains (commercial,
social, fiscal, civil, criminal), procedural deadlines with alerts,
fees and honoraries per case, decisions and results, and a legal
activity PDF report.

Key Features:
-------------
* Litigation cases with parties and legal domains
* Procedural deadlines with alert activities (daily cron)
* Fees and honoraries per case (lawyer, court, expert, travel)
* Decisions, outcomes and controlled case closure
* Legal activity report and case sheet (PDF)
* Multi-company record rules and manager-only closure

Ideal for:
* Legal departments and in-house counsel
* External lawyers and finance teams
* Any organization tracking disputes and litigation
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/litigation_security.xml',
        'security/ir.model.access.csv',
        'views/litigation_views.xml',
        'views/litigation_reports.xml',
        'views/res_config_settings_views.xml',
        'views/litigation_menus.xml',
        'data/litigation_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}