{
    'name': 'Telecom Expense Management',
    'version': '18.0.1.0.0',
    'category': 'Human Resources/Employees',
    'summary': 'Mobile/data/landline lines per employee, plan costs and monthly invoice variance audit',
    'description': """
Telecom Expense Management
==========================

Tame the phone bill.

Features:
---------
* Lines registry: employee, department, provider, number, line type,
  monthly plan cost, contract end date
* Invoice audits per provider and month: expected cost (sum of active
  lines) vs invoiced, variance flagging
* Contract end tracking, multi-company, chatter
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 229.00,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/tel_security.xml',
        'data/tel_data.xml',
        'views/tel_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
