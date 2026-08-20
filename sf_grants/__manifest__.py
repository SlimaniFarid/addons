# -*- coding: utf-8 -*-
{
    'name': 'Grants & Public Funding Management',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Grant programs, calls for projects, application workflow, justified expenses and financial reports',
    'description': """
Grants & Public Funding Management
==================================

Manage subsidies and public funding: reference of programs and
calls for projects (eligibility, deadlines), application files with
a full workflow (draft → submitted → approved → paid → closed or
rejected), justified expenses attached to each application with a
budget control on the granted amount, deadline alerts via cron and
auditable financial reports per program.

Key Features:
-------------
* Programs and calls for projects (funder, budget, deadlines)
* Application workflow with manager-only approvals
* Justified expenses with budget control (granted amount)
* Daily cron deadline and reporting alerts (activity dedup)
* Financial report per program (PDF)
* Aid register (PDF) auditable
* Dashboard of applications by funder type
* Multi-company record rules and permission groups

Ideal for:
* Subsidy / grants officers
* Finance departments (DAF)
* R&D and project teams
* Direction and fund management
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/grant_security.xml',
        'security/ir.model.access.csv',
        'views/grant_views.xml',
        'views/grant_reports.xml',
        'views/res_config_settings_views.xml',
        'views/grant_menus.xml',
        'data/grant_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}