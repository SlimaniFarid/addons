{
    'name': 'Warranty Claims Portal',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Customer self-service warranty claims with SLA tracking and automatic credit note.',
    'description': """
Warranty Claims Portal
======================

Customer self-service warranty claims with SLA tracking and automatic credit note.

**Why you need this**

Stop losing time on spreadsheets and manual tracking.
This module gives your team a dedicated tool inside Odoo,
fully integrated with your existing data.

**Key features**

* One-click workflow from draft to done
* Kanban view for instant visual overview
* Smart filters (My records, To-do) to save time daily
* Overdue detection highlights urgent items automatically
* Responsible user assignment with full tracking

**Getting started**

Install and start creating records immediately.
No configuration needed.

""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 11.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'portal', 'website'],
    'data': ['security/sf_warranty_claims_portal_security.xml', 'security/ir.model.access.csv', 'security/portal_rules.xml', 'data/sf_warranty_claims_portal_sequence.xml', 'views/warranty_claim_views.xml', 'views/sf_warranty_claims_portal_menus.xml', 'views/portal_templates.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
