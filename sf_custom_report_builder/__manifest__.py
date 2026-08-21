{
    'name': 'PDF Report Builder',
    'version': '18.0.1.0',
    'category': 'Productivity',
    'summary': 'Design professional PDF reports without code',
    'description': "Create custom PDF reports (quotes, invoices, delivery slips, purchase orders) with a visual drag-and-drop builder. Add logo, text blocks, tables, signatures, dynamic fields, and conditional sections. No Python/XML coding required. Templates can be assigned per document type and company.",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 19.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'account', 'stock', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'views/report_menus.xml',
        'data/report_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}



