{
    'name': 'Sample & Free Goods Management',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Sample requests to prospects/customers: approval, shipment, feedback and conversion tracking with full cost visibility',
    'description': """
Sample and Free Goods Management
================================

Stop losing track of samples and measure what they actually win.

Features:
---------
* Sample requests: prospect/customer, purpose (evaluation, trade show,
  lab test, press), lines with quantities
* Approval workflow with cost computed from product cost + shipping
* Shipment tracking (picking reference) and follow-up dates
* Feedback records per request: rating, comments, outcome
* Conversion tracking: link to the resulting sale order, won/lost,
  cost per won deal KPI
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 49.75,
    'currency': 'EUR',
    'depends': ['base', 'sale_management', 'stock', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/sample_security.xml',
        'data/sample_data.xml',
        'views/sample_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
