{
    'name': 'Lead Scoring Engine',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Configurable lead scoring rules: engagement, fit, behavior. Auto-prioritize leads for sales teams.',
    'description': """
Lead Scoring Ai
===============

Configurable lead scoring rules: engagement, fit, behavior. Auto-prioritize leads for sales teams.

**Why you need this**

Stop losing time on spreadsheets and manual tracking.
This module gives your team a dedicated tool inside Odoo,
fully integrated with your existing data.

**Key features**

* One-click workflow from draft to done
* Kanban view for instant visual overview
* Smart filters (My records, To-do) save time daily
* Overdue detection highlights urgent items automatically
* Responsible user assignment with full tracking

**Getting started**

Install and start creating records immediately.
No configuration needed.

""",
    'author': 'Ethan Miller',
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': ['security/sf_lead_scoring_ai_security.xml', 'security/ir.model.access.csv', 'data/sf_lead_scoring_ai_sequence.xml', 'views/scoring_rule_views.xml', 'views/lead_score_views.xml', 'views/sf_lead_scoring_ai_menus.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
