{
    'name': 'Production Scheduling Advanced',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Finite capacity scheduling with Gantt view, bottleneck detection and what-if simulation.',
    'description': """
Production Scheduling
=====================

Finite capacity scheduling with Gantt view, bottleneck detection and what-if simulation.

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
    'data': ['security/sf_production_scheduling_security.xml', 'security/ir.model.access.csv', 'data/sf_production_scheduling_sequence.xml', 'views/schedule_plan_views.xml', 'views/schedule_slot_views.xml', 'views/sf_production_scheduling_menus.xml'],
    'images': ['static/description/banner.png'],
    'banner': 'static/description/banner.png',
    'installable': True,
    'application': True,
}
