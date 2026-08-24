{
    'name': 'Lease Accounting (IFRS 16 / ASC 842)',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Right-of-use assets, lease liabilities, PV schedules, monthly journal entries and modifications - IFRS 16 & ASC 842',
    'description': """
Lease Accounting (IFRS 16 / ASC 842)
====================================

Lessee-side lease capitalization native to Odoo Accounting. Replace your
Excel IFRS 16 workbooks with auditable, automated lease schedules.

Core Features:
--------------
* Lease contracts: payments, frequency (monthly/quarterly/annual),
  advance or arrears, incremental borrowing rate (IBR)
* Automatic present-value schedule: interest, principal, closing balance
  per period
* Right-of-Use (ROU) asset: initial measurement = liability
  + initial direct costs + prepaid rent + restoration costs - incentives
* Monthly journal entries generated in one click:
  interest expense + liability repayment + ROU straight-line depreciation
* Modifications & reassessments: re-measure remaining liability at new
  terms, adjust ROU with full audit trail
* Short-term (<= 12 months) and low-value exemptions:
  straight-line expense, no capitalization
* Multi-company with record rules, currencies supported
* Chatter audit trail on every contract and modification

Compliance:
-----------
* IFRS 16 Leases (single lessee model)
* ASC 842 classification field for US GAAP reporting
* Disclosure-ready schedule and contract PDF report

Target Users:
-------------
* CFOs and financial controllers of lessee companies
* Real estate, vehicle, equipment and IT lease portfolios
* Audit preparation without external spreadsheets
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 349.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/lease_security.xml',
        'data/lease_data.xml',
        'views/lease_views.xml',
        'views/lease_reports.xml',
    ],
    'demo': [
        'data/lease_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
