{
    'name': 'Occupational Health & Medical Surveillance',
    'version': '18.0.1.0',
    'category': 'Human Resources',
    'summary': 'Medical visits, aptitudes, restrictions, vaccinations and compliance dashboard',
    'description': """
Occupational Health
===================

Medical visits, aptitudes, restrictions, vaccinations and compliance dashboard

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
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'hr', 'mail'],
    'data': ['security/oh_security.xml', 'security/ir.model.access.csv', 'views/oh_views.xml', 'views/hr_employee_views.xml', 'views/res_config_settings_views.xml', 'views/oh_menus.xml', 'data/oh_cron.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
