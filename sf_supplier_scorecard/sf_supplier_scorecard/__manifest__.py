{
    'name': 'Supplier Scorecard & Quality',
    'version': '18.0.1.0.0',
    'category': 'Purchases',
    'summary': 'Score suppliers on delivery, quality and compliance',
    'description': """
Supplier Scorecard & Quality
============================

Evaluate and rank suppliers with clear scorecards.

Key Features:
-------------
* Periodic scorecards per supplier
* On-time delivery and defect rate KPIs
* Quality and compliance scoring
* Weighted overall score
* Quality issues with resolution tracking
* Supplier ranking by score

Ideal for:
* Procurement teams managing many suppliers
* Quality departments tracking defects
* Vendor performance reviews
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'purchase', 'stock', 'quality'],
    'data': [
        'security/supplier_scorecard_security.xml',
        'security/ir.model.access.csv',
        'views/supplier_scorecard_menus.xml',
        'views/supplier_scorecard_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}