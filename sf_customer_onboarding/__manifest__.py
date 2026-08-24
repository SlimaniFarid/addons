{
    'name': 'Customer Onboarding Workflow',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Structured customer onboarding: document checklist, setup tasks, progress tracking and first-order follow-up',
    'description': """
Customer Onboarding
===================

Turn new customers into active customers without forgetting a step.

Features:
---------
* Onboarding templates with ordered steps (documents, contract,
  account setup, training)
* Onboarding cases per customer with progress % and due dates
* Task workflow with responsible and completion dates
* Multi-company, chatter
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.00,
    'currency': 'EUR',
    'depends': ['base', 'sale', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/cob_security.xml',
        'data/cob_data.xml',
        'views/cob_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
