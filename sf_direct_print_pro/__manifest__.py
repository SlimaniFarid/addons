{
    'name': 'Direct Print PRO',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Print reports & labels directly to network/Bluetooth printers',
    'description': "Print any Odoo report, document, or label directly to your local, Wi-Fi, or Bluetooth printer without downloading PDF. Supports ZPL and PDF formats, automated printing on business events, and cloud print routing. Works with thermal label printers, POS receipt printers, and standard office printers.",
    'author': 'SLIMANI Farid',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 129.0,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'stock', 'sale', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/print_menus.xml',
        'views/print_printer_views.xml',
        'views/print_job_views.xml',
        'views/print_profile_views.xml',
        'data/print_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

