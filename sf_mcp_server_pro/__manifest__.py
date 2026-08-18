{
    'name': 'MCP Server PRO',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Connect AI assistants to your Odoo instance securely',
    'description': "Expose your Odoo data to AI assistants (Claude, ChatGPT, etc.) through a secure Model Context Protocol endpoint.",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 99.0,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'sale', 'stock', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/mcp_server_views.xml',
        'views/mcp_token_views.xml',
        'views/mcp_log_views.xml',
        'data/ir_cron_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}



