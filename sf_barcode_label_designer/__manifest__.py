{
    'name': 'Barcode Label Designer',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Drag-and-drop label designer with barcode/QR support, ZPL and PDF output, batch printing.',
    'description': """
Barcode Label Designer
======================

Drag-and-drop label designer with barcode/QR support, ZPL and PDF output, batch printing.

**Why you need this**

Stop losing time on spreadsheets and manual tracking.
This module gives your team a dedicated tool inside Odoo,
fully integrated with your existing data.

**Key features**

* One-click workflow from draft to done
* Kanban view for instant visual overview
* Smart filters (My records, To-do) to save time daily
* Overdue detection highlights urgent items automatically
* Responsible user assignment with full tracking

**Getting started**

Install and start creating records immediately.
No configuration needed.

""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'website': 'https://www.smartersaas.com',
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'stock'],
    'data': ['security/sf_barcode_label_designer_security.xml', 'security/ir.model.access.csv', 'data/sf_barcode_label_designer_sequence.xml', 'views/label_template_views.xml', 'views/label_print_batch_views.xml', 'views/sf_barcode_label_designer_menus.xml'],
    'installable': True,
    'application': True,
    'images': ['static/description/banner.png'],
}
