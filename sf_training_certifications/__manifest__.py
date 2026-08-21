{
    'name': 'Training & Certification Tracking',
    'version': '19.0.1.0.0',
    'category': 'Human Resources',
    'summary': 'Track employee trainings, sessions, registrations and certifications with expiry alerts',
    'description': """
Training & Certification Tracking
=================================

Centralize employee trainings and certifications with expiry
tracking, renewal alerts and a compliance matrix.

Key Features:
-------------
* Training catalog with categories and mandatory flags
* Session planning and registration management
* Certification issuance with expiration dates
* Expiry and renewal alerts (activities)
* Compliance matrix per employee / training
* Certification and compliance reports

Ideal for:
* HR teams managing training programs
* QHSE teams tracking mandatory certifications
* Auditors preparing ISO / regulatory audits
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 45.00,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'hr', 'mail'],
    'data': [
        'data/training_data.xml',
        'data/training_cron.xml',
        'security/training_security.xml',
        'security/ir.model.access.csv',
        'views/training_menus.xml',
        'views/training_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
