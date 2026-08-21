# -*- coding: utf-8 -*-
{
    'name': 'Youth Sports League & Club Management',
    'version': '19.0.1.0.0',
    'category': 'Sports',
    'summary': 'Youth sports club: registrations, teams, seasons, matches, certificates, family portal',
    'description': '',
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'application': True,
    'installable': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_youth_sports_security.xml', 'security/ir.model.access.csv', 'data/sf_youth_sports_sequence.xml', 'data/sf_youth_sports_cron.xml', 'data/sf_youth_sports_report.xml'],
}
