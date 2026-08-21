{
    'name': 'Direct Print PRO',
    'version': '19.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Print reports & labels directly to network/Bluetooth printers',
    'description': "Print any Odoo report, document, or label directly to your local, Wi-Fi, or Bluetooth printer without downloading PDF. Supports ZPL and PDF formats, automated printing on business events, and cloud print routing. Works with thermal label printers, POS receipt printers, and standard office printers.",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 32.25,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'stock', 'sale', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/print_menus.xml',
        'data/print_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}




