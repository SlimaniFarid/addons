{
    'name': 'Backorder Allocation & Priority',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Allocate scarce stock to open backorders by configurable priority rules (customer segment, value, promised date)',
    'description': """
Backorder Allocation and Priority
=================================

Decide who gets the stock when there is not enough for everyone.

Features:
---------
* Allocation rules: score open backorders by customer priority,
  order value, days late and promised date
* Allocation runs per product: available stock allocated to
  highest-scored deliveries
* Allocation lines with score breakdown and reserved quantity
* Multi-company, chatter
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 57.25,
    'currency': 'EUR',
    'depends': ['base', 'sale', 'stock', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/bo_security.xml',
        'data/bo_data.xml',
        'views/bo_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
