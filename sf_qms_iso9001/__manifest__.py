{
    'name': 'Quality Management System (ISO 9001)',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Full ISO 9001 QMS: NC/CAPA, audits, docs, FMEA, training, management review',
    'description': """Quality Management System (ISO 9001)
===================================

Complete QMS for ISO 9001:2015 certification.

Modules:
- Document Control: versioned docs, approval workflow, distribution, obsolete handling
- Non-Conformity (NC) & CAPA: detection → containment → root cause (5 Whys, Fishbone) → corrective action → effectiveness check → closure
- Internal Audits: plan, checklist, execution, findings, follow-up
- Supplier Quality: approval, scorecards, incoming inspection, SCAR
- FMEA: design (DFMEA) & process (PFMEA) with RPN calculation
- Training & Competence: matrix, records, expiry alerts, qualifications
- Equipment Calibration: schedule, certificates, out-of-cal handling
- Management Review: agenda, inputs (KPIs, NC trends, audit results), outputs, action tracking
- Risk & Opportunity Register: context, interested parties, actions
- Customer Complaints: linked to NC/CAPA, trends, feedback

Features:
- ISO 9001 clause mapping for audit readiness
- Dashboard: open NCs, overdue CAPAs, audit schedule, training compliance
- Email notifications & escalation
- Multi-site / multi-company
- Integration: stock.picking (incoming QC), mrp.production (in-process), maintenance

Certification ready: generates evidence package for registrar.""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 399.0,
    'currency': 'EUR',
    'depends': ['base', 'quality', 'maintenance', 'mrp', 'hr', 'documents'],
    'data': [
        'security/ir.model.access.csv',
        'views/qms_menus.xml',
        'views/qms_nc_views.xml',
        'views/qms_capa_views.xml',
        'views/qms_audit_views.xml',
        'views/qms_doc_views.xml',
        'views/qms_fmea_views.xml',
        'views/qms_training_views.xml',
        'views/qms_review_views.xml',
        'data/qms_data.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}


