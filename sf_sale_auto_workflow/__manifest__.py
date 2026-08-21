{
    'name': 'Sales Auto Workflow',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Automate quotes, deliveries and invoices with configurable rules',
    'description': "Define rules to automatically confirm sales orders, create deliveries, and generate invoices based on payment method, order type, amount, customer, or custom conditions. Reduce manual steps and accelerate order-to-cash cycle.",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 12.25,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'stock', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_auto_menus.xml',
        'data/sale_auto_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}




