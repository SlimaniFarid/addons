{
    'name': 'Change Request & CAB Workflow',
    'version': '19.0.1.0.0',
    'category': 'Operations/Operations',
    'summary': 'IT and operational changes with CAB review, risk levels, rollback plans and post-implementation closure',
    'description': """
Change Request and CAB Workflow
===============================

No surprise changes in production.

Features:
---------
* Change requests: type (IT, process, product, facility), risk level,
  impact analysis, implementation plan, rollback plan
* Change Advisory Board review: votes per member with comments
* Lifecycle: submitted, CAB review, approved, implemented, closed
  (with post-implementation review) or failed/rejected
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.25,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/cr_security.xml',
        'data/cr_data.xml',
        'views/cr_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
