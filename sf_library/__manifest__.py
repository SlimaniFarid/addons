# -*- coding: utf-8 -*-
{
    'name': 'Library & Media Center Management',
    'summary': 'Catalogue, members, loans, returns, late fees and reservations with cron alerts',
    'description': """
Library & Media Center Management
=================================

Structured catalogue of items and media (books, DVDs, CDs,
games, press), library members, dated loans and returns with
availability tracking, computed late days and fines, reservations
with availability lifting and cron alerts.

Key Features:
-------------
* Item catalogue with media types and categories
* Members / users with statuses (draft, active, blocked)
* Loans and returns with available copies computed
* Late days and late fees automatically computed
* Reservations lifted when an item becomes available
* Daily cron alerts for late loans and expiring reservations
* PDF reports: loan receipt / member card, late loans & sanctions
* Per-company access rules

Ideal for:
* Public and school libraries
* Media centers
* Community book clubs
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': '',
    'category': 'Other/Others',
    'version': '18.0.1.0',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'application': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_library_security.xml',
        'security/ir.model.access.csv',
        'views/sf_library_views.xml',
        'views/sf_library_reports.xml',
        'views/res_config_settings_views.xml',
        'views/sf_library_menus.xml',
        'data/actions.xml',
    ],
    'installable': True,
    'auto_install': False,
}
