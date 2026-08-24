{
    'name': 'Customer Health & Churn Risk',
    'version': '19.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Post-sale health scoring per customer: revenue recency, trend and overdue signals with churn risk rating',
    'description': """
Customer Health and Churn Risk
==============================

See which customers are slipping away before they leave.

Features:
---------
* Health refresh per customer: revenue last 12 months, last order
  date and recency, revenue trend vs previous 12 months, overdue
  receivable signal
* Health score 0-100 computed from weighted signals
* Risk rating: healthy, watch, at-risk, churn
* Next action follow-up, owner assignment
* Multi-company, chatter
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 249.00,
    'currency': 'EUR',
    'depends': ['base', 'sale', 'account', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/ch_security.xml',
        'data/ch_data.xml',
        'views/ch_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}
