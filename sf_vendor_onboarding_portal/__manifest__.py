{
    'name': 'Vendor Onboarding Portal',
    'version': '19.0.1.0.0',
    'category': 'Purchase',
    'summary': 'Vendor onboarding portal with document collection, compliance verification and approval workflow.',
    'description': """
Vendor Onboarding Portal
========================

Vendor onboarding portal with document collection, compliance verification and approval workflow.

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
    'data': ['security/sf_vendor_onboarding_portal_security.xml', 'security/ir.model.access.csv', 'security/portal_rules.xml', 'data/sf_vendor_onboarding_portal_sequence.xml', 'views/vendor_onboarding_views.xml', 'views/sf_vendor_onboarding_portal_menus.xml', 'views/portal_templates.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
}
