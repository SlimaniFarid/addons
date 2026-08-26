# -*- coding: utf-8 -*-
{
    'name': 'Yard Management',
    'version': '18.0.1.0.0',
    'category': 'Inventory/Inventory',
    'summary': 'Yard management: trailer inventory with dwell clocks, gate check-in/out, dock assignment, jockey shunts, detention billing',
    'description': """
Yard Management System (YMS)
============================

The yard is the blind spot between the gate and the dock doors. This module
turns it into a live, timestamped operation.

Features:
- Yard map: zones and numbered locations (dock, parking, waiting,
  maintenance, customs, cold)
- Trailer inventory: plate, type, carrier, status, current location,
  automatic dwell clock
- Gate check-in / check-out (manual or QR-ready), driver and carrier logged
- Dock door assignment with occupancy guards
- Directed jockey shunt moves with full timing trail
- Detention & demurrage engine: free time per carrier, warning at 80%,
  chargeable beyond, monthly grouped vendor invoices
- Real-time KPIs: occupancy by zone, average dwell, detention cost of the day
- Daily yard report (PDF)
- Multi-company, multi-yard ready, full chatter audit trail

Stop losing trailers and detention disputes: every gate and door event is
timestamped.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 62.50,
    'currency': 'EUR',
    'application': True,
    'installable': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': [
        'security/sf_yard_management_security.xml',
        'security/ir.model.access.csv',
        'data/sf_yard_sequence.xml',
                
        'models/res_partner.py',
                        'views/sf_yard_views.xml',
                                        'views/sf_yard_menus.xml',        
    ],
}
