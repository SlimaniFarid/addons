{
    'name': 'Universal Approval Engine',
    'version': '19.0.1.0.0',
    'category': 'Operations',
    'summary': 'Reusable multi-step approval workflows for any document (PO, expenses, leave, etc.)',
    'description': """
Universal Approval Engine
=========================

A reusable, document-agnostic approval workflow. Define approval policies
once and apply them to purchase orders, expenses, leave requests, vendor
bills or any other Odoo document.

Key Features:
-------------
* Approval templates with multiple ordered steps
* Automatic step assignment: single approver, manager of creator, or any group
* Per-step rules by amount threshold, company, department or model
* Silent auto-approve steps when conditions are not met
* Rejection with comment, return to draft, edit and re-submit
* Full audit trail: who approved, when, and in which step
* Inbox of pending approvals per user
* Can be attached to native documents (purchase.order, hr.expense, etc.)
* Escalation: remind approvers after a configurable delay

Perfect for:
* Companies formalizing internal control and segregation of duties
* Managers wanting visibility over spends before they happen
* Any team that needs a "sign-off" step on records

Install once, define templates from the UI, attach to any model.
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 199.75,
    'currency': 'EUR',

    'images': ['static/description/banner.png'],
    'depends': ['base', 'mail'],
    'data': [
        'security/approval_security.xml',
        'security/ir.model.access.csv',
        'data/approval_data.xml',
        'views/approval_menus.xml',
        'views/approval_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
