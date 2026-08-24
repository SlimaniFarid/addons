{
    'name': 'KYC / AML Customer Due Diligence',
    'version': '18.0.1.0.0',
    'category': 'Finance/Compliance',
    'summary': 'Customer due diligence register: risk rating, PEP/sanctions screening cycles, UBO declaration and periodic reviews',
    'description': """
KYC / AML Due Diligence Register
================================

Know your customer, prove it to your regulator.

Features:
---------
* KYC files per partner: risk rating (low/medium/high), status
  workflow (pending, approved, rejected, expired)
* PEP / sanctions screening date and periodic refresh cycles
* UBO declaration tracking, document checklist
* Automatic expiry flag and next review scheduling
* Multi-company, chatter audit trail
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 74.75,
    'currency': 'EUR',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/kyc_security.xml',
        'data/kyc_data.xml',
        'views/kyc_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
