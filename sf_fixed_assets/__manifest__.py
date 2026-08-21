{
    'name': 'Fixed Assets Lifecycle',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Assets, categories, depreciation plans and lifecycle tracking',
    'description': """
Fixed Assets Lifecycle
======================

Track the full life of your fixed assets in Odoo.

Key Features:
-------------
* Asset categories with default useful life and method
* Asset records: value, residual value, purchase date
* Straight-line depreciation computed automatically
* Depreciation plan generated per asset
* Asset workflow: draft, in use, disposed, sold
* Book value and accumulated depreciation computed live
* Reports and filters by category, status and location

Ideal for:
* Accountants managing fixed assets
* Facility managers tracking equipment
* Companies needing depreciation schedules
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/fixed_assets_security.xml',
        'security/ir.model.access.csv',
        'data/fixed_assets_data.xml',
        'views/fixed_assets_menus.xml',
        'views/fixed_assets_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
