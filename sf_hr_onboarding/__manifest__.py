# -*- coding: utf-8 -*-
{
    'name': 'Employee Onboarding & Offboarding',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Structured onboarding and offboarding journeys with checklists, tasks and alerts',
    'description': """
Employee Onboarding & Offboarding
=================================

Automate structured arrival and departure journeys for employees:
templates, task checklists, owners, deadlines and reminders.

Key Features:
-------------
* Onboarding and offboarding journey templates
* Automatic program generation when an employee is created
* Tasks with owners, due dates and statuses
* Progress tracking and kanban board
* Equipment preparation and return checks
* Document collection and completion notes
* Automatic reminders for late tasks

Ideal for:
* HR departments
* Managers validating team changes
* IT preparing accounts and equipment
* General services (badges, offices)
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 45.00,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr'],
    'data': [
        'security/onboarding_security.xml',
        'security/ir.model.access.csv',
        'views/onboarding_menus.xml',
        'views/onboarding_views.xml',
        'data/onboarding_cron.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
