{
    'name': 'Procurement Spend Analytics',
    'version': '18.0.1.0.0',
    'category': 'Purchase/Purchase',
    'summary': 'Spend per vendor and category from posted bills, PO coverage and maverick buying detection',
    'description': """
Procurement Spend Analytics
===========================

See where the money goes and who bypasses the process.

Features:
---------
* Analysis runs per period: spend per vendor and product category
  computed from posted vendor bills
* PO coverage: amount linked to purchase orders vs maverick spend
  (bills without PO reference)
* Maverick % per vendor with threshold flagging
* Pivot and graph analysis, multi-company
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 74.75,
    'currency': 'EUR',
    'depends': ['base', 'account', 'purchase', 'product', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/spend_security.xml',
        'data/spend_data.xml',
        'views/spend_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
