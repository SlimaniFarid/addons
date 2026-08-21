# -*- coding: utf-8 -*-
{
    'name': 'HSE — Health & Safety Management',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Incidents, inspections, risk assessments, work permits and PPE tracking',
    'description': """
HSE — Health & Safety Management
=================================

Centralize your occupational health and safety program with
incident management, inspections, risk assessments, work permits
and PPE tracking.

Key Features:
-------------
* Incident declaration with severity, investigation and root cause
* Corrective and preventive action plans with owners and due dates
* Inspections with reusable checklists
* Risk assessment with 5x5 probability x severity matrix
* Work permits (fire, confined space, height) with approval workflow
* PPE tracking with assignment and expiry alerts
* Days without accident counter
* Safety dashboard

Ideal for:
* QHSE departments
* Safety officers and managers
* Industrial, construction, logistics and healthcare sites
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr'],
    'data': [
        'security/hse_security.xml',
        'security/ir.model.access.csv',
        'views/hse_menus.xml',
        'views/hse_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}