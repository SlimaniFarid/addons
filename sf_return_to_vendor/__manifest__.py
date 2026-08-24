{
    'name': 'Return to Vendor (RTV) & Supplier Returns',
    'version': '19.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Defective and excess goods returns to suppliers: RTV orders with dispositions (return/credit/replace/scrap), return pickings and debit note tracking',
    'description': """
Return to Vendor
================

The buy-side twin of customer RMA.

Features:
---------
* RTV orders per vendor with origin (picking / lot) and reason
  (defective, wrong item, overstock, recall, warranty)
* Lines with disposition: return for credit, replace, scrap on site,
  return for repair
* One-click return picking creation to the vendor location with lots
* Debit note reference and settlement tracking
* Cost per line and total RTV value, multi-company, chatter
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'stock', 'purchase', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/rtv_security.xml',
        'data/rtv_data.xml',
        'views/rtv_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
