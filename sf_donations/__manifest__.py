# -*- coding: utf-8 -*-
{
    'name': 'Donations & Charity Management',
    'summary': 'Donation campaigns, pledges, payments and fiscal receipts with automatic reminders',
    'description': """
Donations & Charity Management
===============================

Manage donation campaigns (target and collected amounts), pledges
(one-time or monthly), received payments, fiscal receipts and
automatic reminders for unpaid pledges.

Key Features:
-------------
* Donation campaigns with target and collected amounts
* Pledges (one-time / monthly) linked to campaigns
* Payments received and collected amounts computed
* Fiscal receipts issued by managers
* Automatic reminders for overdue unpaid pledges (cron)
* PDF report per campaign and fiscal receipts register
* Per-company access rules

Ideal for:
* Associations and NGOs
* Fundraising teams and treasurers
* Charity communication teams
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': '',
    'category': 'Other/Others',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'application': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_donations_security.xml',
        'security/ir.model.access.csv',
        'views/sf_donation_views.xml',
        'views/sf_donation_reports.xml',
        'views/res_config_settings_views.xml',
        'views/sf_donation_menus.xml',
        'data/actions.xml',
    ],
    'installable': True,
    'auto_install': False,
}