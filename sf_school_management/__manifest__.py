# -*- coding: utf-8 -*-
{
    'name': 'School Management & Continuing Education (SIS)',
    'version': '19.0.1.0.0',
    'category': 'Education',
    'summary': 'Students, groups/classes, teachers, courses, absences, grades, report cards and tuition fee management',
    'description': """
School Management & Continuing Education (SIS)
==============================================

Manage schools and training centres: students and records,
groups/classes, academic years, teachers, courses and
enrollments, absences with reason and justification, grades and
weighted averages, PDF report cards, tuition fees with payments
and overdue alerts.

Key Features:
-------------
* Students and records (identity, birth date, tutors, status)
* Academic years, groups/classes and teachers
* Courses and student/group enrollments
* Absences with reason and justification
* Grades per student/subject with coefficient and weighted average
* Tuition fees with due dates, payments and overdue alerts (cron)
* PDF report cards and unpaid fees reports
* Multi-company record rules and manager workflow

Ideal for:
* Schools and training centres
* Pedagogical secretaries and teachers
* School directors and accounting departments
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts', 'hr'],
    'data': [
        'security/school_security.xml',
        'security/ir.model.access.csv',
        'views/school_views.xml',
        'views/school_reports.xml',
        'views/res_config_settings_views.xml',
        'views/school_menus.xml',
        'data/school_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
