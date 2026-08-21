{
    'name': 'TikTok Shop Connector',
    'version': '18.0.1.0',
    'category': 'eCommerce',
    'summary': 'Sync products, orders and stock with TikTok Shop',
    'description': "Connect your Odoo instance to TikTok Shop. Synchronize products, inventory, orders, and returns. Supports multiple shops, automated cron sync, webhook handling for real-time updates, and detailed sync logs. Requires TikTok Shop API credentials (App Key, App Secret, Access Token).",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 62.25,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'sale', 'stock', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/tiktokshop_menus.xml',
        'views/tiktokshop_product_views.xml',
        'views/tiktokshop_order_views.xml',
        'views/tiktokshop_sync_log_views.xml',
        'data/tiktokshop_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}



