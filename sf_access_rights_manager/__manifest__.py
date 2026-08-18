{
    'name': 'Access Rights Manager',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Granular permissions without developer mode',
    'description': "Manage fine-grained access rights from a user-friendly interface. Restrict menus, hide fields, disable buttons, block exports, and limit reports per user group — all without writing code or enabling developer mode. Perfect for multi-company environments and role-based security.",
    'author': 'SLIMANI Farid',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 149.0,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/access_menus.xml',
        'views/access_policy_views.xml',
        'views/access_rule_views.xml',
        'data/access_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}



