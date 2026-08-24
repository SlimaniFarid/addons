{
    'name': 'Incident Post-Mortem & Lessons Learned',
    'version': '18.0.1.0.0',
    'category': 'Operations/Operations',
    'summary': 'Operational incident reviews: severity, timeline, root cause, corrective actions and lessons library',
    'description': """
Incident Post-Mortem
====================

Every incident makes you stronger - if you capture it.

Features:
---------
* Incidents with severity (S1-S4), detection/resolution timestamps,
  computed duration and business impact
* Root cause analysis (5 Whys / Fishbone summary)
* Corrective and preventive actions with owners and due dates
* Lessons learned library searchable across incidents
* Multi-company, chatter
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 49.75,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/inc_security.xml',
        'data/inc_data.xml',
        'views/inc_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
