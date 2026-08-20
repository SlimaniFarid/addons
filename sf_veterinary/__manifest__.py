# -*- coding: utf-8 -*-
{
    'name': 'Clinique Vétérinaire & Animaux',
    'summary': 'Veterinary clinic management: animal patients, appointments, vaccinations and hospitalizations',
    'description': """
Clinique Vétérinaire & Animaux
===============================

Manage veterinary clinic operations: complete animal patient records
(species, breed, age, weight, sterilization, allergies), calendar
appointments with clear statuses, vaccination tracking with automatic
due-date reminders, and hospitalization follow-up from admission to
discharge.

Key Features:
-------------
* Animal patient records linked to owners (contacts)
* Calendar appointments with draft/confirm/done/cancelled workflow
* Vaccination booklets with computed due dates and automatic reminders
* Hospitalization tracking (admission, cage, discharge)
* Per-species statistics and pivot views
* PDF reports: vaccination card and hospitalization report
* Per-company access rules and manager-only actions

Ideal for:
* Veterinary clinics
* Veterinarians and assistants
* Clinic secretariat
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
        'security/sf_veterinary_security.xml',
        'security/ir.model.access.csv',
        'views/sf_veterinary_views.xml',
        'views/sf_veterinary_reports.xml',
        'views/res_config_settings_views.xml',
        'views/sf_veterinary_menus.xml',
        'data/actions.xml',
    ],
    'installable': True,
    'auto_install': False,
}
