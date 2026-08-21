# -*- coding: utf-8 -*-
{
    'name': 'GRC â€” Enterprise Risk Management',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Risk register, 5x5 matrix, treatment plans, controls and regulatory mapping',
    'description': """
GRC â€” Enterprise Risk Management
=================================

Governance, risk and compliance for NIS2, DORA, ISO 27001, GDPR
and internal control frameworks.

Key Features:
-------------
* Centralized risk register with categories and owners
* 5x5 probability x impact matrix with residual risk
* Treatment plans with actions, owners and due dates
* Control catalog with pass/fail testing and history
* Regulatory requirement mapping (NIS2, DORA, ISO, GDPR)
* Risk heatmap and dashboard
* Audit-ready reports

Ideal for:
* Risk managers and compliance officers
* Directors and process owners
* Auditors and internal control teams
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 67.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr'],
    'data': [
        'security/risk_security.xml',
        'security/ir.model.access.csv',
        'views/risk_menus.xml',
        'views/risk_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
