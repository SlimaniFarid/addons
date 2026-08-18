{
    'name': 'AI Document Intelligence Hub',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Classify, extract & route documents (invoices, contracts, CVs, claims) with AI',
    'description': """AI Document Intelligence Hub
=============================

Unified document processing: classify + extract + route.

Features:
- Multi-provider AI (Mistral, Gemini, Claude, OpenAI) - BYOK
- Document classification: invoice, contract, CV, claim, PO, expense, other
- Structured extraction per type (vendor, amounts, dates, parties, clauses, skills)
- Automatic routing: invoices → AP, contracts → legal, CVs → HR, claims → support
- Human-in-the-loop review queue with confidence thresholds
- Learning loop: corrections retrain classification/extraction
- Batch processing from email, scanner, portal upload
- Audit log with full traceability

Integrates with:
- account.move (vendor bills)
- hr.applicant (recruitment)
- helpdesk.ticket (claims)
- sale.order (customer POs)
- custom models via extension""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 349.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'hr', 'helpdesk'],
    'data': [
        'security/ir.model.access.csv',
        'views/docintel_menus.xml',
        'data/docintel_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}


