{
    'name': 'Duplicate Records Audit & Merge Assistant',
    'version': '19.0.1.0.0',
    'category': 'Tools',
    'summary': 'Detect duplicate partners (name, email, VAT) with similarity scoring, review groups and track merges',
    'description': """
Duplicate Records Audit
=======================

Clean master data, one scan at a time.

Features:
---------
* Scan strategies: exact name, name + city, same VAT, same email
* Duplicate groups with similarity scoring and member records
* Review workflow: open, merged (via native merge), ignored
* Multi-company safe, chatter on scans
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 179.00,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/dedup_security.xml',
        'data/dedup_data.xml',
        'views/dedup_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
