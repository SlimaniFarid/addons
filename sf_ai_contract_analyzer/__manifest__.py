{
    'name': 'AI Contract Analyzer & Obligations',
    'version': '18.0.1.0.0',
    'category': 'Productivity',
    'summary': 'Extract obligations, dates, risks from contracts (PDF/Word) with AI - auto calendar alerts',
    'description': """AI Contract Analyzer & Obligations
====================================

Turn static contracts into actionable intelligence.

Features:
- Upload PDF/Word/image → AI extracts structured data (Mistral, Gemini, Claude, OpenAI)
- Key entities: parties, effective/termination dates, auto-renewal, notice periods
- Financial: value, payment terms, penalties, price escalation, volume discounts
- Obligations: SLAs, delivery dates, reporting, compliance (GDPR, SOC2, ESG), insurance
- Risk flags: auto-renewal without notice, unlimited liability, unfavorable jurisdiction
- Calendar integration: auto-create alerts for renewals, notice deadlines, price reviews
- Obligation register: searchable, filterable, assignable to owners
- Clause comparison: benchmark against templates, highlight deviations
- Multi-lang support (contracts in any language → English summary)
- Approval workflow: legal review → signatory → counter-party → executed
- Repository: versioned, tagged, full-text search, access control

Integrations:
- sale.order (customer contracts)
- purchase.order (vendor contracts)
- hr.contract (employment)
- fleet.vehicle.lease (leases)
- custom models via extension""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 279.0,
    'currency': 'EUR',
    'depends': ['base', 'mail', 'account', 'hr', 'fleet'],
    'data': [
        'security/ir.model.access.csv',
        'views/contract_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}


