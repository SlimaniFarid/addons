{
    'name': 'First Article Inspection (FAI)',
    'version': '19.0.1.0.0',
    'category': 'Quality/Quality',
    'summary': 'First Article Inspection per AS9102/AS9145 for aerospace/automotive',
    'description': """
First Article Inspection (FAI)
==============================

Complete FAI management per AS9102/AS9145 standards.

Key Features:
-------------
* FAI report generation (Form 1, 2, 3 per AS9102)
* Balloon drawing integration
* Characteristic accountability (100% verification)
* Non-conformance tracking with disposition
* FAI approval workflow (supplier/customer)
* Partial FAI and delta FAI support
* Export to PDF/Excel for customer submission

Ideal for:
* Aerospace suppliers (AS9100/AS9102)
* Automotive suppliers (IATF 16949/AS9145)
* Precision machining and fabrication
* Any industry requiring first article validation
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'quality', 'mrp', 'stock', 'mail'],
    'data': [
        'security/fai_security.xml',
        'security/ir.model.access.csv',
        'data/fai_data.xml',
        'views/fai_menus.xml',
        'views/fai_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
