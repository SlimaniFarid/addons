{
    'name': 'Multi-Company Consolidation',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Consolidate P&L data across companies and currencies',
    'description': """
Multi-Company Consolidation
===========================

Consolidate accounting data across several companies.

Key Features:
-------------
* Consolidation groups with multiple companies
* Period-based consolidation runs
* Account-level entries per company
* Automatic revaluation to the group currency
* Consolidated totals per account
* Exports ready for reporting

Ideal for:
* Holding structures
* Multi-company groups
* Group controllers and CFOs
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'account'],
    'data': [
        'security/consolidation_security.xml',
        'security/ir.model.access.csv',
        'views/consolidation_menus.xml',
        'views/consolidation_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
