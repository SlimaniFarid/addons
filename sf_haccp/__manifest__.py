# -*- coding: utf-8 -*-
{
    'name': 'HACCP Food Safety',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'HACCP food safety: plans, CCP, critical limits, monitoring checks, deviations, corrective actions and auditable PDF registers',
    'description': """
HACCP Food Safety
=================

Sanitary compliance for restaurants, food industry and
distribution: HACCP plans (prerequisites, CCP with critical
limits), monitoring checks (temperature, cleaning) with automatic
deviation detection and corrective actions, nonconformity register
and auditable HACCP PDF registers per site.

Key Features:
-------------
* Sites and prerequisite management (cleaning, water, pest, training, waste, storage)
* HACCP plans by process/zone with steps, hazards, CCP and critical limits
* Planned monitoring checks (temperature, cleaning, pH) with results and automatic status
* Automatic deviation detection out of [target_min, target_max] and nonconformity creation
* Corrective actions and manager-only closure of nonconformities
* Daily cron alerts for scheduled checks without result and overdue nonconformities
* Auditable HACCP PDF register per site
* Multi-company record rules and dedicated user / manager groups

Ideal for:
* Quality and hygiene (HACCP) managers
* Kitchen / production teams
* Food service, catering and distribution
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts', 'hr'],
    'data': [
        'security/haccp_security.xml',
        'security/ir.model.access.csv',
        'views/haccp_views.xml',
        'views/res_config_settings_views.xml',
        'views/haccp_reports.xml',
        'views/haccp_menus.xml',
        'data/haccp_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}