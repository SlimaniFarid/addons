{
    'name': 'Construction BOQ & Subcontractor Billing',
    'version': '18.0.1.0.0',
    'category': 'Operations/Project',
    'summary': 'Bill of Quantities, subcontract management and progress billing (IPC) for construction',
    'description': """Construction BOQ & Subcontractor Billing
====================================

Complete construction project management for contractors and builders.

Key Features:
-------------
* Bill of Quantities (BOQ): multi-discipline itemized estimate (earthwork, concrete, masonry, finishing, electrical, plumbing, HVAC, roofing, other)
* BOQ Workflow: draft, confirmed, in progress, done, cancelled
* Subcontract Management: contractor, contract amount, retention rate, advance, start/end dates
* Subcontract Workflow: draft, confirmed, in progress, closed, cancelled
* Progress Billing (IPC - Interim Payment Certificates): period-based certificates with cumulative quantities and previous certified amounts
* Automatic Calculations: current amount, retention amount, net amount, amount to pay
* Certificate Workflow: draft, confirmed, paid, cancelled
* Mark subcontractor partners for easy filtering
* Company / multi-company ready

Perfect for:
* General contractors and main contractors
* Subcontractors
* Construction project managers
* Building and renovation companies

Features per BOQ line: item code, discipline, description, product link, unit of measure, quantity, unit price.""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'project', 'product', 'account', 'uom'],
    'data': [
        'security/construction_security.xml',
        'security/ir.model.access.csv',
        'data/construction_sequences.xml',
        'views/construction_menus.xml',
        'views/construction_views.xml',
        'reports/certificate_report.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
