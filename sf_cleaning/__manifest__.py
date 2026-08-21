# -*- coding: utf-8 -*-
{
    'name': 'Cleaning Services & Contracts',
    'summary': 'Cleaning service contracts, schedules, interventions, quality checks and invoicing',
    'description': """
Cleaning Services & Contracts
=============================

Manage recurring cleaning service contracts: sites, intervention
frequencies, agent schedules, quality checks and service invoicing.

Key Features:
------------
* Recurring cleaning contracts (draft -> active -> suspended -> done / cancelled)
* Sites linked to clients with team leader assigned
* Agent schedules and order of mission workflows
* Intervention execution recorded by agents
* Quality checks per intervention validated by the team leader
* Automatic TODO alert cron (deduplicated) for overdue frequencies and unassigned agents
* Service invoicing from validated interventions (contract rates)
* Per-company access rules (user / manager)
* PDF reports: order of mission and monthly service summary
* Dedicated settings in res.config.settings
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': '',
    'category': 'Sales',
    'version': '19.0.1.0.0',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'application': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_cleaning_security.xml',
        'security/ir.model.access.csv',
        'views/sf_cleaning_views.xml',
        'views/sf_cleaning_reports.xml',
        'views/res_config_settings_views.xml',
        'views/sf_cleaning_menus.xml',
        'data/actions.xml',
    ],
    'installable': True,
    'auto_install': False,
}
