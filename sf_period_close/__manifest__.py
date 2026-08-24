{
    'name': 'Month-End Close Checklist & Automation',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Structured financial close: checklist templates, task orchestration, sign-offs, blockers and close calendar',
    'description': """
Month-End Close Checklist
=========================

Run your financial close like a production line, not a fire drill.

Features:
---------
* Reusable close checklist templates (per department, sequence,
  relative due days)
* Close periods with generated task lists and progress tracking
* Task workflow: pending, in progress, done, blocked (with blocker
  note), not applicable
* Sign-off per task and final close sign-off
* Blocker dashboard: what stops the close, who owns it
* Close calendar across entities, multi-company
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/close_security.xml',
        'data/close_data.xml',
        'views/close_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
