{
    'name': 'MCP Server PRO',
    'version': '18.0.1.0',
    'category': 'Productivity',
    'summary': 'Connect AI assistants to your Odoo instance securely',
    'description': """
Mcp Server Pro
==============

Connect AI assistants to your Odoo instance securely

**Why you need this**

Stop losing time on spreadsheets and manual tracking.
This module gives your team a dedicated tool inside Odoo,
fully integrated with your existing data.

**Key features**

* One-click workflow from draft to done
* Kanban view for instant visual overview
* Smart filters (My records, To-do) save time daily
* Overdue detection highlights urgent items automatically
* Responsible user assignment with full tracking

**Getting started**

Install and start creating records immediately.
No configuration needed.

""",
    'author': 'Ethan Miller',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'sale', 'stock', 'account'],
    'data': ['security/ir.model.access.csv', 'views/mcp_server_views.xml', 'views/mcp_token_views.xml', 'views/mcp_log_views.xml', 'data/ir_cron_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
