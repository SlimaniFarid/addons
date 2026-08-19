{
    'name': 'Employee Loans & Advances Manager',
    'version': '18.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Manage employee loans and salary advances with auto repayment schedules',
    'description': """
Employee Loans & Advances Manager
=================================

Centralize employee loan and advance requests with approval
workflows and automatic repayment schedules.

Key Features:
-------------
* Loan and advance requests with full approval workflow
* Automatic monthly repayment schedule generation
* Interest rate support
* Balance and paid amount tracking
* Late payment detection
* Per-company advance ceiling
* Loan schedule report

Ideal for:
* HR departments granting loans and advances
* Payroll teams tracking monthly deductions
* Finance teams controlling outstanding advances
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 40.00,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr'],
    'data': [
        'security/employee_loans_security.xml',
        'security/ir.model.access.csv',
        'views/employee_loans_menus.xml',
        'views/employee_loans_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}