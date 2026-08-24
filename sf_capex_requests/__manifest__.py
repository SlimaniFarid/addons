{
    'name': 'CAPEX Request & Investment Approval',
    'version': '19.0.1.0.0',
    'category': 'Finance/Finance',
    'summary': 'Capital expenditure requests with multi-level approvals, ROI/payback fields, budget check and capitalization tracking',
    'description': """
CAPEX Request and Investment Approval
=====================================

Control capital spending before it happens.

Features:
---------
* Investment requests: category, amount, business case, payback and
  ROI inputs, requested vs approved amount
* Multi-level approval chain with per-level approver, comment and date
* Budget check against analytic budget (informational) and annual
  capex envelope per category
* Lifecycle: draft, submitted, approved, rejected, ordered,
  capitalized (asset reference), cancelled
* Capitalization tracking with asset reference and PO link
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/capex_security.xml',
        'data/capex_data.xml',
        'views/capex_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
