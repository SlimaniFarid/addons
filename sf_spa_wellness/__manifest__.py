# -*- coding: utf-8 -*-
{
    'name': 'Spa & Wellness Center Management',
    'version': '18.0.1.0.0',
    'category': 'Healthcare',
    'summary': 'Complete spa management: resource planning, therapists, treatments, packages, memberships',
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
    'data': ['security/sf_spa_wellness_security.xml', 'security/ir.model.access.csv', 'data/sf_spa_wellness_sequence.xml', 'data/sf_spa_wellness_cron.xml', 'data/sf_spa_wellness_report.xml'],
}
