# -*- coding: utf-8 -*-
{
    'name': 'Mental Health & Therapy Practice Management',
    'version': '19.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Mental health practice: patient records, treatment plans, sessions, billing, outcomes',
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
    'data': ['security/sf_mental_health_security.xml', 'security/ir.model.access.csv', 'data/sf_mental_health_sequence.xml', 'data/sf_mental_health_cron.xml', 'data/sf_mental_health_report.xml'],
}
