{
    'name': 'IATF 16949 Automotive Quality Toolkit',
    'version': '19.0.1.0.0',
    'category': 'Manufacturing/Quality',
    'summary': 'Complete AIAG-VDA automotive quality toolchain: DFMEA/PFMEA, Control Plan, APQP, PPAP 18 elements, MSA, SPC',
    'description': """
IATF 16949 Automotive Quality Toolkit
=====================================

Complete AIAG-VDA automotive quality management toolchain native to Odoo Manufacturing & Quality.

Modules Included:
-----------------
1. FMEA (DFMEA & PFMEA) - AIAG-VDA compliant with RPN, action tracking, bidirectional DFMEA↔PFMEA linkage
2. Control Plan - Prototype/Pre-launch/Production phases, auto-generation from PFMEA, linked to Odoo Quality points
3. APQP - 5 phases, 23 standard elements, phase gates, project dashboard with Gantt
4. PPAP - 18 elements (AIAG PPAP-4), submission levels 1-5, PSW auto-fill, package generator
5. MSA / Gauge R&R - Crossed, Nested, Attribute studies with %GRR, ndc, ANOVA, X-bar/R charts
6. SPC - Control charts (X-bar/R, X-bar/S, I-MR, p, np, c, u), Western Electric rules, Cp/Cpk/Pp/Ppk, IoT-ready

Key Features:
-------------
* Bidirectional FMEA ↔ Control Plan linkage (RPN-driven CP generation)
* APQP phase gates with 23-element checklist traceability
* PPAP package generator: single PDF with all 18 elements + PSW auto-filled
* MSA studies linked to Control Plan measurement methods
* Real-time SPC charts with Western Electric/Nelson rule alerts
* IoT endpoint for sensor data push (MQTT/HTTP)
* Multi-company / multi-site security (ir.rule)
* Full audit trail (mail.thread) on all records
* Export PDF/Excel in AIAG standard formats

Integration:
------------
* mrp.production - Link FMEA/CP/PPAP to manufacturing orders
* quality.point / quality.check - Control Plan lines create native Odoo quality points
* maintenance.equipment - MSA studies and SPC charts per equipment
* stock.lot - Traceability from PPAP sample parts to production lots
* res.partner - Customer/supplier quality roles

Certification Ready:
--------------------
Generates complete evidence package for IATF 16949 registrar audits:
- DFMEA/PFMEA with RPN history
- Control Plans (all 3 phases)
- APQP project records with phase gate approvals
- PPAP submissions with customer sign-off
- MSA studies with statistical reports
- SPC control charts with capability indices

Standards Compliance:
---------------------
* AIAG FMEA (4th Edition) / AIAG-VDA FMEA (2019)
* AIAG Control Plan (1st Edition)
* AIAG APQP (3rd Edition)
* AIAG PPAP (4th Edition)
* AIAG MSA (4th Edition)
* AIAG SPC (2nd Edition)
* IATF 16949:2016 Clauses 8.2.3.1, 8.3, 8.5.1, 8.5.6, 9.1.1

Target Industries:
------------------
* Automotive Tier 1/2 suppliers
* Plastic injection molding
* Stamping / metal forming
* Machining / CNC
* Assembly operations
* 3D printing / additive manufacturing
* Composites
""",
    'author': 'Ethan Miller',
    'support': 'tech5262@gmail.com',
    'license': 'OPL-1',
    'price': 449.00,
    'currency': 'EUR',
    'depends': [
        'base',
        'quality',
        'maintenance',
        'mrp',
        'stock',
        'mail',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/iatf_security.xml',
        'data/iatf_data.xml',
        'views/iatf_menus.xml',
        'views/fmea_views.xml',
        'views/control_plan_views.xml',
        'views/apqp_views.xml',
        'views/ppap_views.xml',
        'views/msa_views.xml',
        'views/spc_views.xml',
    ],
    'demo': [
        'data/iatf_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
}