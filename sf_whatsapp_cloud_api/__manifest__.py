{
    'name': 'WhatsApp Business API',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Send WhatsApp messages from Odoo via Meta Cloud API',
    'description': "Integrate WhatsApp Business Cloud API with Odoo Community. Send templated messages from any record (partners, orders, invoices, etc.) with automated workflows for order confirmation, invoice reminders, delivery updates, and more.",
    'author': 'SLIMANI Farid',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 119.0,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'sale', 'account', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/whatsapp_menus.xml',
        'views/whatsapp_account_views.xml',
        'views/whatsapp_template_views.xml',
        'views/whatsapp_message_views.xml',
        'data/whatsapp_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

