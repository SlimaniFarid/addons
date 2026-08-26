{
    'name': 'Equipment Rental & Hire Operations',
    'version': '18.0.1.0',
    'category': 'Operations',
    'summary': 'Equipment cards with calendar availability, rental contracts with tiered pricing, out/in inspections, damages and planned maintenance',
    'description': """
Equipment Rental
================

Equipment cards with calendar availability, rental contracts with tiered pricing, out/in inspections, damages and planned maintenance

**Why you need this**

Stop losing time on spreadsheets and manual tracking.
This module gives your team a dedicated tool inside Odoo,
fully integrated with your existing data.

**Key features**

* One-click workflow from draft to done
* Kanban view for instant visual overview
* Smart filters (My records, To-do) save time daily
* Overdue detection highlights urgent items automatically
* Responsible user assignment with full tracking

**Getting started**

Install and start creating records immediately.
No configuration needed.

""",
    'author': 'Ethan Miller',
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 25.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'contacts', 'account'],
    'data': ['security/sf_rental_security.xml', 'security/ir.model.access.csv', 'data/sf_rental_sequence.xml', 'data/sf_rental_report.xml', 'views/sf_rental_equipment_views.xml', 'views/sf_rental_contract_views.xml', 'views/sf_rental_inspection_views.xml', 'views/sf_rental_maintenance_views.xml', 'views/sf_rental_menus.xml', 'views/report_rental_contract.xml', 'views/report_out_in_ticket.xml', 'views/report_fleet.xml', 'views/res_config_settings_views.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
}
