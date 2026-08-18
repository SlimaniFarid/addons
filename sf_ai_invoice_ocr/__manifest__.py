{
    'name': 'AI Invoice Scanner',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Scan invoices & expenses with AI OCR (Mistral, Gemini, Claude)',
    'description': "Automate invoice and expense entry using AI vision models. Upload PDF/image attachments and extract vendor, date, amounts, line items, taxes. Create vendor bills or expenses with one click. Supports Mistral, Google Gemini, and Anthropic Claude APIs.",
    'author': 'SLIMANI Farid',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 89.0,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'account', 'hr_expense'],
    'data': [
        'security/ir.model.access.csv',
        'views/ai_ocr_menus.xml',
        'views/ai_provider_views.xml',
        'views/ai_ocr_request_views.xml',
        'data/ai_ocr_data.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}

