# Audit Report - Odoo 19.0 Addons

**Date:** 25/08/2026
**Total Modules Audited:** 177

## Executive Summary

- **Modules with security issues (eval/exec):** 0
- **Total eval/exec occurrences:** 0
- **Modules with sudo() usage:** 33
- **Modules with empty methods (stubs):** 0
- **Total stub methods:** 0
- **Modules missing tests:** 34
- **AI modules without real implementation:** 14
- **Duplicate module groups detected:** 0
- **__pycache__ files found:** 0

## Duplicate Modules Analysis

No duplicate modules detected.

## Security Issues - eval()/exec() Usage

No eval/exec issues found.

## sudo() Usage Analysis

| Module | File | Line | Context |
|--------|------|------|---------|
| sf_aql_sampling | sf_aql_sampling\models\sf_aql_inspection.py | 90 | self.env['ir.config_parameter'].sudo() |
| sf_aql_sampling | sf_aql_sampling\models\sf_aql_inspection.py | 108 | self.env['ir.config_parameter'].sudo() |
| sf_aql_sampling | sf_aql_sampling\tests\test_sf_aql_sampling.py | 206 | self.env['ir.config_parameter'].sudo() |
| sf_batch_records | sf_batch_records\models\sf_batch_record.py | 101 | self.env['ir.config_parameter'].sudo() |
| sf_business_travel | sf_business_travel\models\sf_business_travel.py | 159 | self.env['ir.config_parameter'].with_company(company).sudo() |
| sf_cold_chain | sf_cold_chain\models\sf_cold_excursion.py | 114 | self.env['ir.config_parameter'].sudo() |
| sf_cold_chain | sf_cold_chain\tests\test_sf_cold_chain.py | 219 | self.env['ir.config_parameter'].sudo() |
| sf_courier_delivery | sf_courier_delivery\models\sf_courier_delivery.py | 55 | self.env['ir.config_parameter'].sudo() |
| sf_courier_delivery | sf_courier_delivery\models\sf_courier_order.py | 85 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_delivery.py | 152 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_key.py | 76 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_product.py | 31 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_product.py | 34 | self.env['ir.config_parameter'].sudo() |
| sf_digital_delivery | sf_digital_delivery\models\sf_digital_product.py | 43 | self.env['ir.config_parameter'].sudo() |
| sf_direct_print_pro | sf_direct_print_pro\models\print_printer.py | 116 | self.report_id.sudo() |
| sf_dock_appointments | sf_dock_appointments\models\sf_dock_appointment.py | 81 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\models\sf_dock_appointment.py | 132 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\models\sf_dock_appointment.py | 187 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\tests\test_sf_dock_appointments.py | 62 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\tests\test_sf_dock_appointments.py | 70 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\tests\test_sf_dock_appointments.py | 107 | self.env['ir.config_parameter'].sudo() |
| sf_dock_appointments | sf_dock_appointments\tests\test_sf_dock_appointments.py | 165 | self.env['ir.config_parameter'].sudo() |
| sf_equipment_rental | sf_equipment_rental\models\sf_rental_contract.py | 154 | self.env['ir.config_parameter'].sudo() |
| sf_events | sf_events\models\sf_event.py | 95 | scoped.env['ir.config_parameter'].sudo() |
| sf_events | sf_events\tests\test_sf_events.py | 162 | event.sudo() |
| sf_franchise | sf_franchise\models\sf_franchise_declaration.py | 73 | self.env['ir.config_parameter'].sudo() |
| sf_franchise | sf_franchise\models\sf_franchise_declaration.py | 85 | self.env['ir.config_parameter'].sudo() |
| sf_freight_audit | sf_freight_audit\models\sf_freight_dispute.py | 101 | d.invoice_id.sudo() |
| sf_gifts_hospitality | sf_gifts_hospitality\models\sf_gift_hospitality.py | 60 | self.env['ir.config_parameter'].sudo() |
| sf_gifts_hospitality | sf_gifts_hospitality\tests\test_sf_gifts_hospitality.py | 45 | self.env['ir.config_parameter'].sudo() |
| sf_gifts_hospitality | sf_gifts_hospitality\tests\test_sf_gifts_hospitality.py | 54 | self.env['ir.config_parameter'].sudo() |
| sf_ic_netting | sf_ic_netting\ic_models.py | 172 | self.env['ir.config_parameter'].sudo() |
| sf_ic_netting | sf_ic_netting\models\ic_models.py | 172 | self.env['ir.config_parameter'].sudo() |
| sf_invoice_matching | sf_invoice_matching\models\account_move.py | 52 | move.sudo() |
| sf_invoice_matching | sf_invoice_matching\models\account_move.py | 212 | move.sudo() |
| sf_laundry | sf_laundry\models\sf_laundry_order.py | 124 | scoped.env['ir.config_parameter'].sudo() |
| sf_laundry | sf_laundry\models\sf_laundry_order.py | 46 | self.env['ir.config_parameter'].sudo() |
| sf_lease_ifrs16 | sf_lease_ifrs16\lease_contract.py | 370 | self.env['ir.config_parameter'].sudo() |
| sf_lease_ifrs16 | sf_lease_ifrs16\models\lease_contract.py | 370 | self.env['ir.config_parameter'].sudo() |
| sf_mcp_server_pro | sf_mcp_server_pro\controllers\mcp_controller.py | 22 | request.env[model].sudo() |
| sf_mcp_server_pro | sf_mcp_server_pro\controllers\mcp_controller.py | 45 | request.env[model].sudo() |
| sf_mcp_server_pro | sf_mcp_server_pro\controllers\mcp_controller.py | 61 | request.env['mcp.server'].sudo() |
| sf_mcp_server_pro | sf_mcp_server_pro\controllers\mcp_controller.py | 76 | request.env['mcp.request.log'].sudo() |
| sf_parking_management | sf_parking_management\models\sf_parking_site.py | 39 | self.env['ir.config_parameter'].sudo() |
| sf_parking_management | sf_parking_management\models\sf_parking_subscription.py | 66 | self.env['ir.config_parameter'].sudo() |
| sf_period_close | sf_period_close\close_models.py | 158 | rec.period_id.sudo() |
| sf_period_close | sf_period_close\models\close_models.py | 158 | rec.period_id.sudo() |
| sf_pharmacy | sf_pharmacy\models\res_config_settings.py | 13 | self.env['ir.config_parameter'].sudo() |
| sf_pharmacy | sf_pharmacy\models\res_config_settings.py | 22 | self.env['ir.config_parameter'].sudo() |
| sf_pharmacy | sf_pharmacy\models\sf_pharmacy_batch.py | 178 | self.env['ir.config_parameter'].sudo() |
| sf_pharmacy | sf_pharmacy\tests\test_sf_pharmacy.py | 183 | self.env['ir.config_parameter'].sudo() |
| sf_pharmacy | sf_pharmacy\tests\test_sf_pharmacy.py | 198 | self.env['ir.config_parameter'].sudo() |
| sf_policy_acknowledgment | sf_policy_acknowledgment\models\sf_policy.py | 144 | self.env['ir.config_parameter'].sudo() |
| sf_product_reviews | sf_product_reviews\models\sf_product_review.py | 47 | self.env['sale.order.line'].sudo() |
| sf_product_reviews | sf_product_reviews\models\sf_product_review.py | 71 | self.env['ir.config_parameter'].sudo() |
| sf_product_reviews | sf_product_reviews\models\sf_product_review.py | 73 | self.env['ir.config_parameter'].sudo() |
| sf_restaurant | sf_restaurant\models\sf_restaurant_reservation.py | 117 | scoped.env['ir.config_parameter'].sudo() |
| sf_rework_management | sf_rework_management\models\sf_rework_order.py | 85 | self.env['ir.config_parameter'].sudo() |
| sf_rework_management | sf_rework_management\models\sf_rework_order.py | 151 | self.env['ir.config_parameter'].sudo() |
| sf_rework_management | sf_rework_management\tests\test_sf_rework_management.py | 162 | self.env['ir.config_parameter'].sudo() |
| sf_salon_beauty | sf_salon_beauty\models\sf_salon_service.py | 33 | self.env['ir.config_parameter'].sudo() |
| sf_salon_beauty | sf_salon_beauty\models\sf_salon_staff.py | 23 | self.env['ir.config_parameter'].sudo() |
| sf_salon_beauty | sf_salon_beauty\tests\test_sf_salon_beauty.py | 185 | self.env['ir.config_parameter'].sudo() |
| sf_salon_beauty | sf_salon_beauty\tests\test_sf_salon_beauty.py | 186 | self.env['ir.config_parameter'].sudo() |
| sf_senior_living | sf_senior_living\wizard\billing_wizard.py | 249 | self.env['ir.config_parameter'].sudo() |
| sf_senior_living | sf_senior_living\wizard\billing_wizard.py | 277 | self.env['ir.config_parameter'].sudo() |
| sf_staffing | sf_staffing\models\sf_staffing_mission.py | 189 | self.env['ir.config_parameter'].sudo() |
| sf_store_credit | sf_store_credit\models\sf_store_credit.py | 180 | self.env['ir.config_parameter'].sudo() |
| sf_trade_promotions | sf_trade_promotions\models\sf_trade_claim.py | 71 | self.env['ir.config_parameter'].sudo() |
| sf_trade_promotions | sf_trade_promotions\models\sf_trade_program.py | 74 | expired.sudo() |
| sf_travel_agency | sf_travel_agency\models\res_config_settings.py | 23 | self.env['ir.config_parameter'].sudo() |
| sf_travel_agency | sf_travel_agency\models\sf_travel_package.py | 80 | self.env['ir.config_parameter'].sudo() |
| sf_travel_agency | sf_travel_agency\models\sf_travel_reservation.py | 41 | self.env['ir.config_parameter'].sudo() |
| sf_utility_billing | sf_utility_billing\models\sf_utility_invoice.py | 68 | self.env['ir.config_parameter'].sudo() |
| sf_utility_billing | sf_utility_billing\models\sf_utility_meter.py | 58 | self.env['ir.config_parameter'].sudo() |
| sf_utility_billing | sf_utility_billing\tests\test_sf_utility_billing.py | 141 | self.env['ir.config_parameter'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 13 | request.env['purchase.order'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 23 | request.env['purchase.order'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 33 | request.env['purchase.order'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 43 | request.env['purchase.order'].sudo() |
| sf_vendor_portal | sf_vendor_portal\controllers\portal.py | 53 | request.env['purchase.order'].sudo() |

## Empty Methods (Stubs)

No empty methods found.

## Modules Missing Tests

sf_access_review, sf_backorder_priority, sf_bank_stmt_import_pro, sf_capex_requests, sf_change_requests, sf_credit_insurance, sf_customer_health, sf_customer_onboarding, sf_customer_rebates, sf_data_dedup, sf_facility_management, sf_fx_hedging, sf_iatf_quality_suite, sf_ic_netting, sf_incident_postmortem, sf_inventory_aging, sf_kyc_aml, sf_lease_ifrs16, sf_load_planning, sf_management_reporting, sf_period_close, sf_policy_waivers, sf_price_change_mgmt, sf_product_eol, sf_purchase_price_analysis, sf_quality_coa, sf_renewal_management, sf_return_to_vendor, sf_sample_management, sf_spend_analytics, sf_supplier_rebates, sf_telecom_expense, sf_transfer_pricing, sf_yard_management

## AI Modules - Implementation Gap Analysis

| Module | Claims | Has External Deps | Has API Key Config |
|--------|--------|-------------------|---------------------|
| sf_ai_contract_analyzer | Extract obligations, dates, risks from contracts (PDF/Word) with AI - auto calendar alerts AI Contra... | False | False |
| sf_ai_demand_forecast | ML-powered demand forecasting for inventory optimization AI Demand Forecasting
=====================... | False | False |
| sf_ai_doc_intelligence | Classify, extract & route documents (invoices, contracts, CVs, claims) with AI AI Document Intellige... | False | False |
| sf_automation_builder | Zapier-like visual builder: triggers â†’ actions â†’ conditions for Odoo models + external APIs Visu... | False | False |
| sf_cold_chain | Monitor temperature excursions on cold storage sites and transport trips with alerts and reports ... | False | False |
| sf_complaint_8d | 8D methodology: team formation, root cause, corrective actions, CAPA tracking and supplier notificat... | False | False |
| sf_first_article_inspection | First Article Inspection per AS9102/AS9145 for aerospace/automotive 
First Article Inspection (FAI)
... | False | False |
| sf_iatf_quality_suite | Complete AIAG-VDA automotive quality toolchain: DFMEA/PFMEA, Control Plan, APQP, PPAP 18 elements, M... | False | False |
| sf_lead_scoring_ai | Configurable lead scoring rules: engagement, fit, behavior. Auto-prioritize leads for sales teams. ... | False | False |
| sf_mcp_server_pro | Connect AI assistants to your Odoo instance securely ... | False | False |
| sf_preventive_maintenance_pro | PM scheduling by meter reading or time triggers, work order auto-generation and compliance calendar.... | False | False |
| sf_privacy_rgpd | Data protection register (RGPD): treatments, processors, DPIA, breach and data subject rights manage... | False | False |
| sf_training_certifications | Track employee trainings, sessions, registrations and certifications with expiry alerts 
Training & ... | False | False |
| sf_warranty_claims_portal | Customer self-service warranty claims with SLA tracking and automatic credit note. ... | False | False |

## Manifest Issues

No manifest parsing issues.

## Versioned __pycache__ Files

No __pycache__ files found.

## Module-by-Module Details

### sf_access_review

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Periodic user access reviews: campaign per scope, per-user group review with keep/revoke decisions and evidence

### sf_access_rights_manager

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Granular permissions without developer mode

### sf_agriculture

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 13
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Farms, plots, campaigns, cultures, treatments, harvests and inputs register for agriculture

### sf_ai_contract_analyzer

- **Models:** None
- **Depends:** base, mail, account, hr, fleet
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Extract obligations, dates, risks from contracts (PDF/Word) with AI - auto calendar alerts

### sf_ai_demand_forecast

- **Models:** None
- **Depends:** base, stock, sale
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** ML-powered demand forecasting for inventory optimization

### sf_ai_doc_intelligence

- **Models:** None
- **Depends:** base, mail, account, hr, helpdesk
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Classify, extract & route documents (invoices, contracts, CVs, claims) with AI

### sf_ai_invoice_ocr

- **Models:** None
- **Depends:** base, account, hr_expense
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Scan invoices & expenses with AI OCR (Mistral, Gemini, Claude)

### sf_approval_engine

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Reusable multi-step approval workflows for any document (PO, expenses, leave, etc.)

### sf_aql_sampling

- **Models:** None
- **Depends:** base, mail, product, stock, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Statistical acceptance sampling: AQL inspection plans, lot inspections, defect recording and accept/reject decisions

### sf_asset_depreciation_pro

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Multi-method depreciation (straight-line, declining, units) with component accounting and revaluation.

### sf_automation_builder

- **Models:** None
- **Depends:** base, mail, web
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Zapier-like visual builder: triggers â†’ actions â†’ conditions for Odoo models + external APIs

### sf_backorder_priority

- **Models:** None
- **Depends:** base, sale, stock, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Allocate scarce stock to open backorders by configurable priority rules (customer segment, value, promised date)

### sf_bank_loans

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track bank loans, calculated amortization schedules, drawdowns, early repayments and covenants with alerts

### sf_bank_stmt_import_pro

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 9
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Import any bank statement: MT940, CAMT.053, OFX, QIF or any bank CSV - per-bank templates, duplicate detection, multi-currency

### sf_barcode_label_designer

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Drag-and-drop label designer with barcode/QR support, ZPL and PDF output, batch printing.

### sf_batch_records

- **Models:** None
- **Depends:** base, mail, product, stock, contacts
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Electronic batch production records: materials, steps, parameters, deviations, QA review and lot release

### sf_business_continuity

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Resilience ISO 22301: critical processes BIA, continuity strategies, recovery plans, exercises and review alerts

### sf_business_travel

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Employee travel requests, approval workflow, itinerary lines, budget tracking and mission orders

### sf_capex_requests

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Capital expenditure requests with multi-level approvals, ROI/payback fields, budget check and capitalization tracking

### sf_cash_flow_forecast

- **Models:** None
- **Depends:** base, account, purchase
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Forecast cash position, track receivables/payables and avoid liquidity gaps

### sf_change_requests

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** IT and operational changes with CAB review, risk levels, rollback plans and post-implementation closure

### sf_cleaning

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Cleaning service contracts, schedules, interventions, quality checks and invoicing

### sf_cold_chain

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Monitor temperature excursions on cold storage sites and transport trips with alerts and reports

### sf_community_center

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Community center management: spaces, activities, memberships, ticketing, grants

### sf_complaint_8d

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** 8D methodology: team formation, root cause, corrective actions, CAPA tracking and supplier notification.

### sf_compliance_register

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track licenses, permits, certifications and insurance expirations with alerts

### sf_consolidation

- **Models:** None
- **Depends:** base, account
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Consolidate P&L data across companies and currencies

### sf_construction_boq

- **Models:** None
- **Depends:** base, project, product, account, uom
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Bill of Quantities, subcontract management and progress billing (IPC) for construction

### sf_corporate_capital

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Shareholders, share classes, capital movements (issue/transfer/buyback), issued shares, cap table and share certificates

### sf_corporate_secretary

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Corporate secretariat: organs, AG/board meetings, convocations, resolutions, votes, minutes, written decisions and regulatory deadlines

### sf_correspondence

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Incoming and outgoing correspondence register with routing, response deadlines and registered mail tracking

### sf_courier_delivery

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Pickup/delivery requests, courier assignment, routes, delivery proof (photo/signature), failures, returns and invoicing

### sf_cpq_configurator

- **Models:** None
- **Depends:** base, sale, product, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configure custom products, compute prices and generate quotes

### sf_creche

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Children, enrollments, daily attendance, room capacity control and monthly hourly billing

### sf_credit_insurance

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Insurer policies, approved buyer limits with coverage %, and bad-debt claims with indemnity tracking

### sf_custom_report_builder

- **Models:** None
- **Depends:** base, sale, account, stock, purchase
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Design professional PDF reports without code

### sf_customer_credit_limits

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automated credit limit enforcement with blocking, escalation workflow and exposure dashboard.

### sf_customer_health

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Post-sale health scoring per customer: revenue recency, trend and overdue signals with churn risk rating

### sf_customer_onboarding

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured customer onboarding: document checklist, setup tasks, progress tracking and first-order follow-up

### sf_customer_portal_pro

- **Models:** None
- **Depends:** base, website, sale, account, portal, payment
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** B2B/B2C portal: invoices, payments, subscriptions, returns, tickets, documents

### sf_customer_rebates

- **Models:** None
- **Depends:** base, account, sale, product, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sell-side rebate deals (retro %, turnover bonus, per unit) with accrual from invoices and credit note settlement

### sf_data_dedup

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Detect duplicate partners (name, email, VAT) with similarity scoring, review groups and track merges

### sf_debt_collection

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Aging analysis, collection cases, dunning plans and payment promises

### sf_digital_delivery

- **Models:** None
- **Depends:** base, mail, contacts, product, sale
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Digital products, automatic license key generation, expirable download links and digital delivery tracking

### sf_direct_print_pro

- **Models:** None
- **Depends:** base, stock, sale, account, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Print reports & labels directly to network/Bluetooth printers

### sf_dock_appointments

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Dock registry and truck appointment scheduling with time windows, arrival tracking and no-show detection

### sf_document_expiry_tracker

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track employee document expiry with automated renewal reminders.

### sf_donations

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Donation campaigns, pledges, payments and fiscal receipts with automatic reminders

### sf_edi_einvoicing

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Peppol, Factur-X, ViDA, ANSI X12, CFDI, KSeF - certified e-invoicing & EDI

### sf_employee_loans

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage employee loans and salary advances with auto repayment schedules

### sf_energy_monitoring

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track energy and utility consumption per site and meter with ESG reporting

### sf_equipment_rental

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 14
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Equipment cards with calendar availability, rental contracts with tiered pricing, out/in inspections, damages and planned maintenance

### sf_esg_reporting

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Collect, validate and report ESG indicators (environment, social, governance) per company and period for CSRD compliance

### sf_events

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Events, sessions, speakers, registrations and ticketing, badge check-in, budget and revenue tracking

### sf_export_documents

- **Models:** None
- **Depends:** base, mail, contacts, sale, product
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Export pack documents, Incoterms, completeness control and dossier workflow

### sf_facility_management

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sites, rooms and bookings with capacity control and conflict detection

### sf_field_dispatch_board

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Dispatch board with skills matching, route optimization, SLA timers and mobile check-in/out.

### sf_field_service_offline

- **Models:** None
- **Depends:** base, industry_fsm, stock, mail
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** True offline-first mobile app for field technicians with background sync

### sf_first_article_inspection

- **Models:** None
- **Depends:** base, quality, mrp, stock, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** First Article Inspection per AS9102/AS9145 for aerospace/automotive

### sf_fixed_assets

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Assets, categories, depreciation plans and lifecycle tracking

### sf_franchise

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Franchise contracts, declared sales, automatic royalty calculation, invoicing and payment tracking

### sf_freight_audit

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Audit carrier invoices against contracts and shipments: detect overcharges, manage disputes, recover money

### sf_freight_costing

- **Models:** None
- **Depends:** base, stock, account
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track carriers, cost formulas and freight on pickings

### sf_fuel_management

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Fuel cards, fills with L/100km consumption tracking, tanks with receipts and anomaly alerts

### sf_fx_hedging

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Open FX exposure per currency from receivables/payables, forward contracts with settlement gain/loss tracking

### sf_gifts_hospitality

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Anti-bribery register of gifts and hospitality given or received with approval threshold

### sf_grants

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Grant programs, calls for projects, application workflow, justified expenses and financial reports

### sf_gym_fitness

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 13
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Gym memberships, plans, group classes, sessions, attendances and payments with automatic alerts

### sf_haccp

- **Models:** None
- **Depends:** base, mail, contacts, hr
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** HACCP food safety: plans, CCP, critical limits, monitoring checks, deviations, corrective actions and auditable PDF registers

### sf_hotel_pms

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Hospitality & Reservations (light PMS)

### sf_hr_onboarding

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Structured onboarding and offboarding journeys with checklists, tasks and alerts

### sf_hse_management

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Incidents, inspections, risk assessments, work permits and PPE tracking

### sf_iatf_quality_suite

- **Models:** None
- **Depends:** base, quality, maintenance, mrp, stock, mail, product
- **Python Files:** 16
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Complete AIAG-VDA automotive quality toolchain: DFMEA/PFMEA, Control Plan, APQP, PPAP 18 elements, MSA, SPC

### sf_ic_netting

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Match open intercompany balances across entities, compute net positions per company pair and generate settlement entries

### sf_incident_postmortem

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Operational incident reviews: severity, timeline, root cause, corrective actions and lessons library

### sf_insurance_management

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Insurance policies, premiums, guarantees, renewals and claims with indemnities

### sf_intercompany_invoicing

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automated intercompany invoices with multi-book accounting, currency conversion and elimination entries.

### sf_inventory_aging

- **Models:** None
- **Depends:** base, stock, product, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Stock aging buckets from last movement, slow-mover detection and obsolescence provision suggestions

### sf_investment_management

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Portfolios, investment lines, valuations, dividends and coupons, maturity alerts and PDF performance reports

### sf_invoice_matching

- **Models:** None
- **Depends:** base, sale, purchase, purchase_stock, account, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Automatic purchase order / receipt / invoice reconciliation with tolerances and exceptions

### sf_it_asset_management

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track IT equipment, software licenses, assignments and warranties

### sf_kyc_aml

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Customer due diligence register: risk rating, PEP/sanctions screening cycles, UBO declaration and periodic reviews

### sf_laundry

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Deposit vouchers and items, treatment statuses, per-piece pricing, pickup/delivery and customer history

### sf_lead_scoring_ai

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Configurable lead scoring rules: engagement, fit, behavior. Auto-prioritize leads for sales teams.

### sf_lease_ifrs16

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 7
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Right-of-use assets, lease liabilities, PV schedules, monthly journal entries and modifications - IFRS 16 & ASC 842

### sf_library

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Catalogue, members, loans, returns, late fees and reservations with cron alerts

### sf_litigation

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Legal cases and pre-litigation: cases and parties, domains, procedural deadlines with alerts, fees and honoraries, decisions and results, legal activity PDF report

### sf_load_planning

- **Models:** None
- **Depends:** base, stock, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Build truck loads from pickings with capacity checks (weight, volume, pallets), route stops and load manifest

### sf_management_reporting

- **Models:** None
- **Depends:** base, account, sale, purchase, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Board-ready monthly pack: revenue, costs, margin KPIs vs previous month with commentary

### sf_marketplace_hub

- **Models:** None
- **Depends:** base, sale, account, product
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Multi-vendor marketplace: channels, vendors, listings and orders in one hub

### sf_mcp_server_pro

- **Models:** None
- **Depends:** base, mail, sale, stock, account
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Connect AI assistants to your Odoo instance securely

### sf_medical_practice

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Patient files, conflict-free appointment agenda, consultations, prescriptions and vital signs with computed BMI

### sf_membership_advanced

- **Models:** None
- **Depends:** base, mail, sale, account, website
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage members, subscriptions & renewals for associations and NGOs

### sf_mental_health

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mental health practice: patient records, treatment plans, sessions, billing, outcomes

### sf_mes_andons

- **Models:** None
- **Depends:** base, mrp, stock, maintenance, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Real-time Andon alerts, escalation and response tracking for shop floor

### sf_mes_shop_floor

- **Models:** None
- **Depends:** base, mrp, stock, quality
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track work orders, stations, downtime and quality on the floor

### sf_nps_feedback

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** NPS survey campaigns with automated detractor follow-up, trend analysis and team scorecards.

### sf_occupational_health

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Medical visits, aptitudes, restrictions, vaccinations and compliance dashboard

### sf_packaging_consigns

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Returnable packaging consigns: deposit types, parks per site, emissions/returns linked to deliveries, invoiced deposits, return rate and stock alerts

### sf_parking_management

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 13
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Parking sites and zones, spaces, recurring subscriptions, tickets, entry/exit and occupancy statistics

### sf_period_close

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Structured financial close: checklist templates, task orchestration, sign-offs, blockers and close calendar

### sf_pharmacy

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Pharmacy management: products, batches, expiries and prescription dispensations

### sf_policy_acknowledgment

- **Models:** None
- **Depends:** base, mail, contacts, hr
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Versioned internal policies, employee assignment, acknowledgment sign-off, reminders and coverage rate

### sf_policy_waivers

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Time-boxed policy waivers with risk assessment, compensating controls and approval workflow

### sf_preventive_maintenance_pro

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** PM scheduling by meter reading or time triggers, work order auto-generation and compliance calendar.

### sf_price_change_mgmt

- **Models:** None
- **Depends:** base, product, sale, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan, announce and apply price increases: product lines with old/new price, delta %, effective dates and one-click application

### sf_price_matrix

- **Models:** None
- **Depends:** base, sale, product, account
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Tiered pricing and discount matrix per customer category

### sf_privacy_rgpd

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Data protection register (RGPD): treatments, processors, DPIA, breach and data subject rights management

### sf_process_routing

- **Models:** None
- **Depends:** base, mrp, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Alternative routing selection based on conditions, capacity, and quality

### sf_product_compliance

- **Models:** None
- **Depends:** base, mail, product, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Regulatory compliance of products (CE, RoHS, REACH, UL, FDA): regulations, requirements, compliance dossiers and certificates with expiry alerts

### sf_product_eol

- **Models:** None
- **Depends:** base, product, sale, stock, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Phase-out planning: EOL announcements, last-time-buy dates, replacement mapping, open order checks and sale blocking

### sf_product_pim

- **Models:** None
- **Depends:** base, product, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Central product data, families, attributes, completeness score and channel publications

### sf_product_reviews

- **Models:** None
- **Depends:** base, mail, product, sale, contacts
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Customer product reviews, moderation workflow, verified purchases and aggregated ratings

### sf_production_planning

- **Models:** None
- **Depends:** base, mail, mrp
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Master production schedule with Gantt, priorities and work center load

### sf_production_scheduling

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Finite capacity scheduling with Gantt view, bottleneck detection and what-if simulation.

### sf_project_margin

- **Models:** None
- **Depends:** base, project, sale, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track project budgets, costs and margins live

### sf_promotional_pricing_engine

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Time-based promotional pricing with customer segments, volume tiers and margin protection rules.

### sf_psa

- **Models:** None
- **Depends:** base, sale, project, hr, account, mail
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage engagements, resources and time for services teams

### sf_purchase_price_analysis

- **Models:** None
- **Depends:** base, account, purchase, product, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** PPV per product/vendor vs standard cost from posted bills, price change history and increase alerts

### sf_purchase_requisition

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Purchase requisition with multi-level approval chains, budget checking and vendor suggestion.

### sf_qms_iso9001

- **Models:** None
- **Depends:** base, quality, maintenance, mrp, hr, documents
- **Python Files:** 17
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Full ISO 9001 QMS: NC/CAPA, audits, docs, FMEA, training, management review

### sf_quality_coa

- **Models:** None
- **Depends:** base, stock, quality, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Generate certificates of analysis per delivery: test parameters, specifications, results and approval workflow

### sf_quality_inspection

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mobile-first quality inspection checklists with photo capture and non-conformance escalation.

### sf_real_estate

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Properties, leases, tenants and rent invoicing in one place

### sf_renewal_management

- **Models:** None
- **Depends:** base, sale, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Renewal pipeline for customer contracts: notice deadlines, auto-renew flags, churn risk and renewal outcomes

### sf_rental_billing

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Recurring rental billing: contracts, automatic invoicing cycles, proration, deposit management.

### sf_resource_planning

- **Models:** None
- **Depends:** base, project, hr, resource
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Allocate resources to projects, track capacity and avoid overload

### sf_restaurant

- **Models:** None
- **Depends:** base, mail, contacts, product
- **Python Files:** 14
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Restaurant and cafe management: tables, reservations, menus, kitchen orders and revenue tracking

### sf_return_to_vendor

- **Models:** None
- **Depends:** base, stock, purchase, account, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Defective and excess goods returns to suppliers: RTV orders with dispositions (return/credit/replace/scrap), return pickings and debit note tracking

### sf_returns_rma

- **Models:** None
- **Depends:** base, sale, stock, account, delivery
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Unified returns portal for eCommerce, POS, B2B, marketplaces with auto-approval rules

### sf_revenue_recognition

- **Models:** None
- **Depends:** base, account, sale, account_asset
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** ASC 606 / IFRS 15 compliant revenue recognition for subscriptions and contracts

### sf_rework_management

- **Models:** None
- **Depends:** base, mail, product, stock, contacts
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Track rework orders, operations and scrap with cost computation and escalation alerts

### sf_risk_management

- **Models:** None
- **Depends:** base, hr
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Risk register, 5x5 matrix, treatment plans, controls and regulatory mapping

### sf_safety_stock

- **Models:** None
- **Depends:** base, stock, product, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Optimal safety stock levels and reorder points from real demand

### sf_sale_auto_workflow

- **Models:** None
- **Depends:** base, sale, stock, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automate quotes, deliveries and invoices with configurable rules

### sf_sales_commission

- **Models:** None
- **Depends:** base, sale, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Flexible commission plans, auto-computed from paid invoices and tracked per salesperson

### sf_sales_routes

- **Models:** None
- **Depends:** base, sale, crm
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Plan field sales routes, track visits, territories and objectives

### sf_salon_beauty

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 13
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Appointments, staff availability, packages, commissions and billing for salons and beauty studios

### sf_sample_management

- **Models:** None
- **Depends:** base, sale_management, stock, product, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sample requests to prospects/customers: approval, shipment, feedback and conversion tracking with full cost visibility

### sf_school_management

- **Models:** None
- **Depends:** base, mail, contacts, hr
- **Python Files:** 16
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Students, groups/classes, teachers, courses, absences, grades, report cards and tuition fee management

### sf_senior_living

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 20
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Complete management for senior residences, EHPAD, retirement communities

### sf_service_contracts

- **Models:** None
- **Depends:** base, sale, account, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Service contracts, SLA tiers and breach tracking

### sf_shop_floor_terminal

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Shop floor terminal for work order tracking, time logging, quantity reporting and scrap entry.

### sf_spa_wellness

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 27
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Complete spa management: resource planning, therapists, treatments, packages, memberships

### sf_spend_analytics

- **Models:** None
- **Depends:** base, account, purchase, product, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Spend per vendor and category from posted bills, PO coverage and maverick buying detection

### sf_staffing

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 14
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Temporary work and placement agency management: candidates, clients, needs, missions, contracts, timesheets and invoicing.

### sf_stock_barcode_advanced

- **Models:** None
- **Depends:** base, stock, product
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Advanced barcode scanning for inventory operations

### sf_store_credit

- **Models:** None
- **Depends:** base, mail, contacts, sale
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Customer store credit accounts, reusable credit grants, usage, adjustments, expirations and balances

### sf_subscription_dunning

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Automated dunning: retry schedules, escalation emails and revenue recovery dashboard.

### sf_supplier_rebates

- **Models:** None
- **Depends:** base, account, purchase, product, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Vendor rebate deals (volume bonus, retro %), automatic accrual from posted bills, claims and settlement tracking

### sf_supplier_scorecard

- **Models:** None
- **Depends:** base, purchase, stock, quality
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Score suppliers on delivery, quality and compliance

### sf_telecom_expense

- **Models:** None
- **Depends:** base, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Mobile/data/landline lines per employee, plan costs and monthly invoice variance audit

### sf_tender_management

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage RFQ/RFI/RFP and public tenders with criteria scoring and justified award

### sf_tiktokshop_connector

- **Models:** None
- **Depends:** base, sale, stock, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Sync products, orders and stock with TikTok Shop

### sf_time_attendance

- **Models:** None
- **Depends:** base, hr, hr_attendance, mail
- **Python Files:** 8
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Shifts, overtime, late arrivals and attendance analytics

### sf_tool_management

- **Models:** None
- **Depends:** base, mrp, stock, maintenance, quality
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track tools, gauges, fixtures with calibration, wear, and lifecycle

### sf_traceability

- **Models:** None
- **Depends:** base, stock, product, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Full batch traceability, recall events and product history

### sf_trade_finance

- **Models:** None
- **Depends:** base, sale, purchase, account, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Letters of credit, bank guarantees and documentary collections with key dates and documents

### sf_trade_promotions

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Trade promotion programs, budgets, customer claims, validation workflow and ROI tracking

### sf_training_certifications

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 14
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Track employee trainings, sessions, registrations and certifications with expiry alerts

### sf_transfer_pricing

- **Models:** None
- **Depends:** base, account, mail
- **Python Files:** 5
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Intercompany arm-length pricing policies (CUP, cost-plus, resale-minus, TNMM), variance analysis and Master File / Local File documentation

### sf_travel_agency

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Manage travel packages, providers, reservations and margin analysis.

### sf_utility_billing

- **Models:** None
- **Depends:** base, mail, uom, contacts, account
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Delivery points and meters registry, reading campaigns, tiered tariffs and consumption invoices

### sf_vehicle_workshop

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Vehicles, intervention requests, repair orders with operations and parts, full cost per vehicle and urgency alerts

### sf_vendor_contracts

- **Models:** None
- **Depends:** base, product, mail
- **Python Files:** 12
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Manage supplier contracts, clauses, amounts, expirations and renewals with alerts

### sf_vendor_onboarding_portal

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Vendor onboarding portal with document collection, compliance verification and approval workflow.

### sf_vendor_portal

- **Models:** None
- **Depends:** base, purchase, portal, account, mail
- **Python Files:** 10
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** Yes
- **Stubs:** 0
- **Summary:** Self-service vendor portal: RFQs, quotations, orders and invoices online

### sf_veterinary

- **Models:** None
- **Depends:** base, mail, contacts
- **Python Files:** 11
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Veterinary clinic management: animal patients, appointments, vaccinations and hospitalizations

### sf_visitor_access

- **Models:** None
- **Depends:** base, hr, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Visitor check-in/out, badges, zones, safety rules and real-time presence register

### sf_warehouse_heatmap

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Activity heatmap for slotting optimization: pick frequency, travel distance and ABC classification.

### sf_warranty_claims_portal

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 6
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Customer self-service warranty claims with SLA tracking and automatic credit note.

### sf_warranty_management

- **Models:** None
- **Depends:** base, mail, product, stock, sale, account
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Product warranties, claims with automatic eligibility check and motivated decisions

### sf_waste_management

- **Models:** None
- **Depends:** base, mail, contacts, web
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Waste tracking slips (BSD), sites and waste codes

### sf_wave_picking

- **Models:** None
- **Depends:** base, stock, stock_picking_batch, mail
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Group pickings into waves and release them efficiently

### sf_whatsapp_cloud_api

- **Models:** None
- **Depends:** base, mail, sale, account, stock
- **Python Files:** 7
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Send WhatsApp messages from Odoo via Meta Cloud API

### sf_yard_management

- **Models:** None
- **Depends:** base, mail, account, stock
- **Python Files:** 10
- **Has Tests:** No
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Yard management: trailer inventory with dwell clocks, gate check-in/out, dock assignment, jockey shunts, detention billing

### sf_youth_sports

- **Models:** None
- **Depends:** base, mail, contacts, account
- **Python Files:** 9
- **Has Tests:** Yes
- **Has eval/exec:** No
- **Has sudo():** No
- **Stubs:** 0
- **Summary:** Youth sports club: registrations, teams, seasons, matches, certificates, family portal

