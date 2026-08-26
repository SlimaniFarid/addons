{
    'name': 'School Management & Continuing Education (SIS)',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Students, groups/classes, teachers, courses, absences, grades, report cards and tuition fee management',
    'description': """
School Management
=================

Students, groups/classes, teachers, courses, absences, grades, report cards and tuition fee management

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
    'license': 'OPL-1',
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts', 'hr'],
    'data': ['security/school_security.xml', 'security/ir.model.access.csv', 'views/school_views.xml', 'views/school_reports.xml', 'views/res_config_settings_views.xml', 'views/school_menus.xml', 'data/school_data.xml'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
