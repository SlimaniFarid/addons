{
    'name': 'AI Invoice Scanner',
    'version': '18.0.1.0',
    'category': 'Accounting',
    'summary': 'Scan invoices & expenses with AI OCR (Mistral, Gemini, Claude)',
    'description': """
Ai Invoice Ocr
==============

Scan invoices & expenses with AI OCR (Mistral, Gemini, Claude)

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
    'license': 'OPL-1',
    'price': 17.95,
    'currency': 'EUR',
    'depends': ['base', 'account', 'hr_expense'],
    'data': ['security/ir.model.access.csv', 'views/ai_ocr_menus.xml', 'data/ai_ocr_data.xml'],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
