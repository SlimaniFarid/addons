{
    'name': 'Time & Attendance System',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Shifts, overtime, late arrivals and attendance analytics',
    'description': """
Time & Attendance System
========================

Advanced time and attendance tracking in Odoo.

Key Features:
-------------
* Employee shift patterns per weekday
* Automatic overtime computation
* Late arrival and early departure detection
* Monthly attendance summary per employee
* Expected hours from shift patterns
* Absence tracking

Ideal for:
* HR teams monitoring punctuality
* Payroll managers computing overtime
* Companies with complex shift schedules
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr', 'hr_attendance', 'mail'],
    'data': [
        'security/time_attendance_security.xml',
        'security/ir.model.access.csv',
        'data/time_attendance_data.xml',
        'views/time_attendance_menus.xml',
        'views/time_attendance_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
