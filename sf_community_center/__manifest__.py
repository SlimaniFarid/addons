# -*- coding: utf-8 -*-
{
    'name': 'Community Center & Recreation Management',
    'version': '19.0.1.0.0',
    'category': 'Services',
    'summary': 'Community center management: spaces, activities, memberships, ticketing, grants',
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
    'data': ['security/sf_community_center_security.xml', 'security/ir.model.access.csv', 'data/sf_community_center_sequence.xml', 'data/sf_community_center_cron.xml', 'data/sf_community_center_report.xml'],
}
