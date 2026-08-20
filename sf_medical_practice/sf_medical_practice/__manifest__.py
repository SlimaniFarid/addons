# -*- coding: utf-8 -*-
{
    'name': 'Medical Practice & Patients',
    'summary': 'Patient files, conflict-free appointment agenda, consultations, prescriptions and vital signs with computed BMI',
    'description': """
Medical Practice & Patients
===========================

Lightweight patient files, a conflict-free appointment agenda,
consultations with diagnosis, prescriptions with dosage and
computed vital signs (BMI) for medical practices.

Key Features:
-------------
* Centralized patient files (identity, allergies, insurance)
* Appointment agenda without overlapping slots per practitioner
* Consultations with diagnosis (draft → done → closed)
* Prescriptions with dosage (draft → issued → closed)
* Vital signs with computed BMI (weight / height squared)
* Automated reminder activities for upcoming unconfirmed appointments
* Per-company access rules (user / manager)

Ideal for:
* Medical practices and private clinics
* Practitioners and medical secretaries
* Nursing staff
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': 'https://tech5262.com',
    'category': 'Other/Others',
    'version': '18.0.1.0.0',
    'license': 'OPL-1',
    'price': 62.50,
    'application': True,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'contacts'],
    'data': [
        'security/sf_medical_practice_security.xml',
        'security/ir.model.access.csv',
        'views/medical_views.xml',
        'views/res_config_settings_views.xml',
        'views/medical_menus.xml',
        'views/medical_reports.xml',
        'data/actions.xml',
    ],
    'installable': True,
    'auto_install': False,
}