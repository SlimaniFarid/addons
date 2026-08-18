{
    'name': 'Barcode & Warehouse',
    'version': '18.0.1.0.0',
    'category': 'Inventory',
    'summary': 'Advanced barcode scanning for inventory operations',
    'description': "Enhance warehouse operations with advanced barcode scanning. Scan products, lots, serial numbers, packages, and locations on receipts, deliveries, and inventory adjustments. Supports multiple barcode formats (EAN13, UPC, QR, Code128, GS1), mobile-friendly scanning interface, and automated putaway/picking routes.",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 99.0,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'stock', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/barcode_menus.xml',
        'data/barcode_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}



