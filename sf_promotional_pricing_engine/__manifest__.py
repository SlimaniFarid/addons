{
    'name': 'Promotional Pricing Engine',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Time-based promotional pricing with customer segments, volume tiers and margin protection rules.',
    'description': """
Promotional Pricing Engine
==========================

Time-based promotional pricing with customer segments, volume tiers and margin protection rules.

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
    'data': ['security/sf_promotional_pricing_engine_security.xml', 'security/ir.model.access.csv', 'data/sf_promotional_pricing_engine_sequence.xml', 'views/promo_rule_views.xml', 'views/sf_promotional_pricing_engine_menus.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
