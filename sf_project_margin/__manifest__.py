{
    'name': 'Project Margin & Budget Control',
    'version': '18.0.1.0',
    'category': 'Project/Project',
    'summary': 'Track project budgets, costs and margins live',
    'description': """
Project Margin & Budget Control
===============================

Track project budgets, costs and margins live.

Key Features:
-------------
* Revenue and cost budgets per project
* Budget items by category
* Automatic margin and margin percentage
* Threshold warnings on margin drop
* Linked to native project and analytic accounts
* Reports for project portfolio margin

Ideal for:
* Agencies and studios
* Implementation partners
* Engineering and consulting projects
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'project', 'sale', 'account'],
    'data': [
        'security/project_margin_security.xml',
        'security/ir.model.access.csv',
        'views/project_margin_menus.xml',
        'views/project_margin_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}