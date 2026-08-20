# -*- coding: utf-8 -*-
{
    'name': 'Business Continuity & BIA (PCA)',
    'version': '18.0.1.0.0',
    'category': 'Operations',
    'summary': 'Resilience ISO 22301: critical processes BIA, continuity strategies, recovery plans, exercises and review alerts',
    'description': """
Business Continuity & BIA (PCA)
===============================

Manage the company resilience program (ISO 22301): register critical
processes with a Business Impact Analysis (criticality, RTO, RPO and
financial impact), define continuity strategies, publish recovery
plans with steps and owners, run exercises with results and get
automatic review reminders before the plans expire.

Key Features:
-------------
* Business Impact Analysis: critical processes with RTO / RPO
* Criticality levels and financial impact per process
* Continuity strategies (alternate site, workaround, outsourcing...)
* Recovery plans: version, summary, steps, resources, owner
* Plan workflow: draft, published, tested, updated
* Exercises and tests with results and improvement findings
* Periodic plan review alerts via daily cron (configurable delay)
* BIA and Recovery Plan PDF reports
* Dashboard by criticality and status

Ideal for:
* BCP / PCA managers and directors
* Risk and security officers
* Process owners
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/bcp_security.xml',
        'security/ir.model.access.csv',
        'views/bcp_views.xml',
        'views/bcp_reports.xml',
        'views/res_config_settings_views.xml',
        'views/bcp_menus.xml',
        'data/bcp_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}