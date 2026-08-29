{
    'name': 'IATF 16949 Automotive Quality Toolkit',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Complete AIAG-VDA automotive quality toolchain: DFMEA/PFMEA, Control Plan, APQP, PPAP 18 elements, MSA, SPC',
    'description': """
Iatf Quality Suite
==================

Complete AIAG-VDA automotive quality toolchain: DFMEA/PFMEA, Control Plan, APQP, PPAP 18 elements, MSA, SPC

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
    'license': 'OPL-1',
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'quality', 'maintenance', 'mrp', 'stock', 'mail', 'product'],
    'data': ['security/ir.model.access.csv', 'security/iatf_security.xml', 'data/iatf_data.xml', 'views/iatf_menus.xml', 'views/fmea_views.xml', 'views/control_plan_views.xml', 'views/apqp_views.xml', 'views/ppap_views.xml', 'views/msa_views.xml', 'views/spc_views.xml'],
    'images': ['static/description/banner.png'],
    'demo': ['data/iatf_demo.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
