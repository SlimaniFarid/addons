{
    'name': 'Monthly Management Report Pack',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Finance',
    'summary': 'Board-ready monthly pack: revenue, costs, margin KPIs vs previous month with commentary',
    'description': """
Monthly Management Reporting
============================

From ledger to boardroom in one click.

Features:
---------
* Monthly report per entity: revenue, COGS/vendor costs, gross margin
  computed from posted invoices and bills
* KPI lines vs previous month with delta %
* Commentary section per report
* Finalize workflow, multi-company
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'sale', 'purchase', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/mr_security.xml',
        'data/mr_data.xml',
        'views/mr_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
