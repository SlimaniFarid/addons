# Odoo 18 -> 19 Migration Impact Analysis

**Modules to migrate:** 358
**Date:** 25/08/2026

## Module Complexity Ranking (by issue count)

| Module | Issues | Priority |
|--------|--------|----------|
| sf_access_request_workflow | 2 | LOW |
| sf_accrual_proposals | 2 | LOW |
| sf_accrual_reversal_auto | 2 | LOW |
| sf_anniversary_reminders | 2 | LOW |
| sf_api_integration_log | 2 | LOW |
| sf_asset_count_campaign | 2 | LOW |
| sf_asset_disposal_request | 2 | LOW |
| sf_backup_verification_log | 2 | LOW |
| sf_bank_fee_analytics | 2 | LOW |
| sf_bank_reconciliation_rules | 2 | LOW |
| sf_batch_job_monitor | 2 | LOW |
| sf_blanket_order_release | 2 | LOW |
| sf_bom_change_request | 2 | LOW |
| sf_budget_virement | 2 | LOW |
| sf_budget_vs_actual_alerts | 2 | LOW |
| sf_business_glossary | 2 | LOW |
| sf_business_requirement | 2 | LOW |
| sf_capacity_forecast_sales | 2 | LOW |
| sf_capacity_planner | 2 | LOW |
| sf_capital_expenditure_plan | 2 | LOW |
| sf_carrier_performance | 2 | LOW |
| sf_certificate_requests | 2 | LOW |
| sf_change_freeze_calendar | 2 | LOW |
| sf_checklist_library | 2 | LOW |
| sf_churn_prediction_rules | 2 | LOW |
| sf_commission_clawback | 2 | LOW |
| sf_committee_decisions | 2 | LOW |
| sf_company_car_policy | 2 | LOW |
| sf_compensation_benchmark | 2 | LOW |
| sf_competitive_intel_register | 2 | LOW |
| sf_compliance_calendar | 2 | LOW |
| sf_compliance_obligation | 2 | LOW |
| sf_contract_compliance_audit | 2 | LOW |
| sf_credit_note_reasons | 2 | LOW |
| sf_cross_sell_engine | 2 | LOW |
| sf_crossdock_operations | 2 | LOW |
| sf_currency_exposure_map | 2 | LOW |
| sf_customer_advisory_board | 2 | LOW |
| sf_customer_advocacy_program | 2 | LOW |
| sf_customer_care_coaching | 2 | LOW |
| sf_customer_care_coaching_plan | 2 | LOW |
| sf_customer_care_escalation | 2 | LOW |
| sf_customer_care_escalation_dashboard | 2 | LOW |
| sf_customer_care_escalation_matrix | 2 | LOW |
| sf_customer_care_escalation_rules | 2 | LOW |
| sf_customer_care_escalation_tracker | 2 | LOW |
| sf_customer_care_journey | 2 | LOW |
| sf_customer_care_program | 2 | LOW |
| sf_customer_care_qa_review | 2 | LOW |
| sf_customer_care_qa_scorecard | 2 | LOW |
| sf_customer_care_satisfaction | 2 | LOW |
| sf_customer_care_satisfaction_survey | 2 | LOW |
| sf_customer_care_sla | 2 | LOW |
| sf_customer_care_sla_breach | 2 | LOW |
| sf_customer_care_sla_dashboard | 2 | LOW |
| sf_customer_care_sla_rules | 2 | LOW |
| sf_customer_care_survey | 2 | LOW |
| sf_customer_care_training | 2 | LOW |
| sf_customer_care_training_plan | 2 | LOW |
| sf_customer_care_workforce | 2 | LOW |
| sf_customer_care_workforce_plan | 2 | LOW |
| sf_customer_care_workload | 2 | LOW |
| sf_customer_churn_analytics | 2 | LOW |
| sf_customer_complaint_praise | 2 | LOW |
| sf_customer_contract_renewal_forecast | 2 | LOW |
| sf_customer_contract_renewal_pipeline | 2 | LOW |
| sf_customer_covenant_tracker | 2 | LOW |
| sf_customer_document_vault | 2 | LOW |
| sf_customer_escalation_matrix | 2 | LOW |
| sf_customer_expansion_tracker | 2 | LOW |
| sf_customer_feedback_actions | 2 | LOW |
| sf_customer_feedback_analytics | 2 | LOW |
| sf_customer_health_scoring | 2 | LOW |
| sf_customer_incident_comms | 2 | LOW |
| sf_customer_journey_analytics | 2 | LOW |
| sf_customer_journey_map | 2 | LOW |
| sf_customer_journey_mapper | 2 | LOW |
| sf_customer_journey_stage | 2 | LOW |
| sf_customer_onboarding_checklist | 2 | LOW |
| sf_customer_onboarding_cost | 2 | LOW |
| sf_customer_onboarding_docs | 2 | LOW |
| sf_customer_pain_point | 2 | LOW |
| sf_customer_payment_behavior | 2 | LOW |
| sf_customer_payment_plan | 2 | LOW |
| sf_customer_portal_tasks | 2 | LOW |
| sf_customer_pricing_requests | 2 | LOW |
| sf_customer_priority_matrix | 2 | LOW |
| sf_customer_profitability_rank | 2 | LOW |
| sf_customer_reference_program | 2 | LOW |
| sf_customer_reference_tracker | 2 | LOW |
| sf_customer_revenue_trend | 2 | LOW |
| sf_customer_risk_score | 2 | LOW |
| sf_customer_satisfaction_trend | 2 | LOW |
| sf_customer_segment_rules | 2 | LOW |
| sf_customer_segments_rules | 2 | LOW |
| sf_customer_visit_reports | 2 | LOW |
| sf_cycle_count_scheduler | 2 | LOW |
| sf_damaged_goods_log | 2 | LOW |
| sf_data_quality_check | 2 | LOW |
| sf_deal_desk_request | 2 | LOW |
| sf_decision_log | 2 | LOW |
| sf_demand_planning_review | 2 | LOW |
| sf_disciplinary_action | 2 | LOW |
| sf_dividend_register | 2 | LOW |
| sf_document_approval_hybrid | 2 | LOW |
| sf_dr_plan_tracker | 2 | LOW |
| sf_dropship_operations | 2 | LOW |
| sf_ehs_inspection_schedule | 2 | LOW |
| sf_emergency_purchase_log | 2 | LOW |
| sf_employee_1on1_tracker | 2 | LOW |
| sf_employee_asset_return | 2 | LOW |
| sf_employee_engagement_action | 2 | LOW |
| sf_employee_referral | 2 | LOW |
| sf_employee_skill_gap | 2 | LOW |
| sf_employee_survey | 2 | LOW |
| sf_energy_meter_readings | 2 | LOW |
| sf_energy_saving_tracker | 2 | LOW |
| sf_environmental_waste_tracking | 2 | LOW |
| sf_equipment_utilization | 2 | LOW |
| sf_exit_interviews | 2 | LOW |
| sf_expiry_alert_manager | 2 | LOW |
| sf_external_audit_tracker | 2 | LOW |
| sf_field_service_checklist | 2 | LOW |
| sf_field_service_customer_satisfaction | 2 | LOW |
| sf_field_service_dispatch | 2 | LOW |
| sf_field_service_parts | 2 | LOW |
| sf_financial_covenant_monitor | 2 | LOW |
| sf_financial_ratio_dashboard | 2 | LOW |
| sf_first_piece_validation | 2 | LOW |
| sf_fixed_asset_transfer | 2 | LOW |
| sf_freight_quote_compare | 2 | LOW |
| sf_fx_hedge_accounting | 2 | LOW |
| sf_fx_reval_scheduler | 2 | LOW |
| sf_grievance_tracker | 2 | LOW |
| sf_incident_oncall | 2 | LOW |
| sf_intercompany_balance_check | 2 | LOW |
| sf_intercompany_loan | 2 | LOW |
| sf_interim_billing_tracker | 2 | LOW |
| sf_internal_audit_program | 2 | LOW |
| sf_internal_mobility | 2 | LOW |
| sf_internship_tracker | 2 | LOW |
| sf_inventory_abc_classification | 2 | LOW |
| sf_inventory_accuracy_rate | 2 | LOW |
| sf_inventory_count_variance | 2 | LOW |
| sf_inventory_revaluation | 2 | LOW |
| sf_inventory_shrinkage_tracker | 2 | LOW |
| sf_inventory_turnover_analysis | 2 | LOW |
| sf_inventory_writeoff_register | 2 | LOW |
| sf_invoice_discounting | 2 | LOW |
| sf_it_asset_lifecycle | 2 | LOW |
| sf_it_capacity_planning | 2 | LOW |
| sf_job_costing_snapshot | 2 | LOW |
| sf_key_account_plans | 2 | LOW |
| sf_knowledge_articles | 2 | LOW |
| sf_kpi_target_register | 2 | LOW |
| sf_late_payment_interest | 2 | LOW |
| sf_line_balancing_review | 2 | LOW |
| sf_maintenance_cost_tracker | 2 | LOW |
| sf_maintenance_intake | 2 | LOW |
| sf_maintenance_schedule_optimizer | 2 | LOW |
| sf_marketing_budget_tracker | 2 | LOW |
| sf_marketing_campaign_roi | 2 | LOW |
| sf_meeting_minutes | 2 | LOW |
| sf_mgmt_fee_billing | 2 | LOW |
| sf_min_order_enforcement | 2 | LOW |
| sf_minmax_review | 2 | LOW |
| sf_multi_site_price_harmony | 2 | LOW |
| sf_nonconformance_cost | 2 | LOW |
| sf_obsolescence_forecast | 2 | LOW |
| sf_onboarding_cost | 2 | LOW |
| sf_oncall_schedule | 2 | LOW |
| sf_ooo_calendar | 2 | LOW |
| sf_operator_skill_matrix | 2 | LOW |
| sf_order_freeze_windows | 2 | LOW |
| sf_overtime_preapproval | 2 | LOW |
| sf_packaging_spec_register | 2 | LOW |
| sf_pallet_sscc_labels | 2 | LOW |
| sf_payment_milestone_engine | 2 | LOW |
| sf_payroll_deadline_tracker | 2 | LOW |
| sf_peak_season_planning | 2 | LOW |
| sf_po_acknowledgment | 2 | LOW |
| sf_po_amendment_log | 2 | LOW |
| sf_po_budget_check | 2 | LOW |
| sf_policy_exception_tracker | 2 | LOW |
| sf_prepaid_amortization | 2 | LOW |
| sf_probation_review_tracker | 2 | LOW |
| sf_procurement_savings_tracker | 2 | LOW |
| sf_product_lifecycle_stage | 2 | LOW |
| sf_product_margin_matrix | 2 | LOW |
| sf_product_return_rate | 2 | LOW |
| sf_product_return_reasons | 2 | LOW |
| sf_production_capacity_plan | 2 | LOW |
| sf_production_capacity_review | 2 | LOW |
| sf_production_capacity_whatif | 2 | LOW |
| sf_production_downtime_pareto | 2 | LOW |
| sf_production_line_efficiency | 2 | LOW |
| sf_production_meeting_actions | 2 | LOW |
| sf_production_oee_calculator | 2 | LOW |
| sf_production_oee_dashboard | 2 | LOW |
| sf_production_oee_tracker | 2 | LOW |
| sf_production_order_priority | 2 | LOW |
| sf_production_order_sequencing | 2 | LOW |
| sf_production_scenarios | 2 | LOW |
| sf_production_schedule_alert | 2 | LOW |
| sf_production_scrap_analytics | 2 | LOW |
| sf_production_scrap_pareto | 2 | LOW |
| sf_production_trial_tracking | 2 | LOW |
| sf_production_waste_tracker | 2 | LOW |
| sf_production_yield_analysis | 2 | LOW |
| sf_production_yield_tracker | 2 | LOW |
| sf_project_change_request | 2 | LOW |
| sf_project_charter | 2 | LOW |
| sf_project_lessons_learned | 2 | LOW |
| sf_project_milestone_tracker | 2 | LOW |
| sf_project_portfolio_board | 2 | LOW |
| sf_project_resource_plan | 2 | LOW |
| sf_project_risk_log | 2 | LOW |
| sf_project_stakeholder | 2 | LOW |
| sf_provision_register | 2 | LOW |
| sf_purchase_approval_matrix | 2 | LOW |
| sf_purchase_contract_compliance | 2 | LOW |
| sf_purchase_envelope | 2 | LOW |
| sf_purchase_order_aging | 2 | LOW |
| sf_purchase_requisition_analytics | 2 | LOW |
| sf_purchase_requisition_template | 2 | LOW |
| sf_quality_alert_aging | 2 | LOW |
| sf_quality_alert_auto_assign | 2 | LOW |
| sf_quality_alert_escalation | 2 | LOW |
| sf_quality_audit_program | 2 | LOW |
| sf_quality_cost_tracker | 2 | LOW |
| sf_quality_document_control | 2 | LOW |
| sf_quality_document_control_sys | 2 | LOW |
| sf_quality_hold_register | 2 | LOW |
| sf_quality_inspection_mobile2 | 2 | LOW |
| sf_quality_inspection_plan | 2 | LOW |
| sf_quality_inspection_planner | 2 | LOW |
| sf_quality_pareto_analyzer | 2 | LOW |
| sf_quality_pareto_update | 2 | LOW |
| sf_quality_trend_dashboard | 2 | LOW |
| sf_quote_followup_cadence | 2 | LOW |
| sf_receiving_discrepancy_log | 2 | LOW |
| sf_recurring_cost_register | 2 | LOW |
| sf_recurring_revenue_register | 2 | LOW |
| sf_recurring_task_templates | 2 | LOW |
| sf_regulatory_watch | 2 | LOW |
| sf_remote_work_requests | 2 | LOW |
| sf_replenishment_review | 2 | LOW |
| sf_retention_schedule | 2 | LOW |
| sf_revenue_backlog_tracker | 2 | LOW |
| sf_revenue_leak_detector | 2 | LOW |
| sf_revenue_leakage_analyzer | 2 | LOW |
| sf_revenue_milestone | 2 | LOW |
| sf_revenue_protection_plan | 2 | LOW |
| sf_runbook_library | 2 | LOW |
| sf_safety_inspections | 2 | LOW |
| sf_safety_training_tracker | 2 | LOW |
| sf_sales_asset_library | 2 | LOW |
| sf_sales_battle_rhythm | 2 | LOW |
| sf_sales_battlecard | 2 | LOW |
| sf_sales_capacity_model | 2 | LOW |
| sf_sales_coaching_dashboard | 2 | LOW |
| sf_sales_coaching_effectiveness | 2 | LOW |
| sf_sales_coaching_log | 2 | LOW |
| sf_sales_coaching_plan | 2 | LOW |
| sf_sales_commission_plan | 2 | LOW |
| sf_sales_commission_simulation | 2 | LOW |
| sf_sales_commission_statement | 2 | LOW |
| sf_sales_content_library | 2 | LOW |
| sf_sales_enablement_tracker | 2 | LOW |
| sf_sales_forecast_accuracy | 2 | LOW |
| sf_sales_forecast_category | 2 | LOW |
| sf_sales_gamification | 2 | LOW |
| sf_sales_hiring_funnel | 2 | LOW |
| sf_sales_hiring_plan | 2 | LOW |
| sf_sales_hiring_tracker | 2 | LOW |
| sf_sales_huddle_notes | 2 | LOW |
| sf_sales_hygiene_audit | 2 | LOW |
| sf_sales_onboarding_plan | 2 | LOW |
| sf_sales_order_acknowledgment | 2 | LOW |
| sf_sales_pipeline_review | 2 | LOW |
| sf_sales_play_execution | 2 | LOW |
| sf_sales_playbook | 2 | LOW |
| sf_sales_target_cascade | 2 | LOW |
| sf_sales_territory_planner | 2 | LOW |
| sf_sales_territory_review | 2 | LOW |
| sf_scrap_reason_analytics | 2 | LOW |
| sf_sell_through_reporting | 2 | LOW |
| sf_service_catalog | 2 | LOW |
| sf_service_level_agreement_monitor | 2 | LOW |
| sf_shift_swap_board | 2 | LOW |
| sf_sla_pause_tracking | 2 | LOW |
| sf_software_license_renewals | 2 | LOW |
| sf_spare_parts_minmax | 2 | LOW |
| sf_special_price_approval | 2 | LOW |
| sf_stock_adjustment_approval | 2 | LOW |
| sf_succession_plan | 2 | LOW |
| sf_supplier_audit_program | 2 | LOW |
| sf_supplier_audit_scheduler | 2 | LOW |
| sf_supplier_bank_change_alert | 2 | LOW |
| sf_supplier_capacity_check | 2 | LOW |
| sf_supplier_capacity_forecast | 2 | LOW |
| sf_supplier_capacity_planner | 2 | LOW |
| sf_supplier_capacity_review | 2 | LOW |
| sf_supplier_contract_database | 2 | LOW |
| sf_supplier_contract_renewal | 2 | LOW |
| sf_supplier_contract_renewal_alert | 2 | LOW |
| sf_supplier_contract_renewal_tracker | 2 | LOW |
| sf_supplier_diversity_tracker | 2 | LOW |
| sf_supplier_invoice_3way_match | 2 | LOW |
| sf_supplier_invoice_3way_match3 | 2 | LOW |
| sf_supplier_invoice_accuracy | 2 | LOW |
| sf_supplier_invoice_matching | 2 | LOW |
| sf_supplier_leadtime_audit | 2 | LOW |
| sf_supplier_negotiation_prep | 2 | LOW |
| sf_supplier_onboarding_checklist | 2 | LOW |
| sf_supplier_onboarding_portal | 2 | LOW |
| sf_supplier_pareto_abc | 2 | LOW |
| sf_supplier_payment_optimization | 2 | LOW |
| sf_supplier_payment_terms | 2 | LOW |
| sf_supplier_performance_dashboard | 2 | LOW |
| sf_supplier_performance_review | 2 | LOW |
| sf_supplier_pricing_benchmark | 2 | LOW |
| sf_supplier_pricing_history | 2 | LOW |
| sf_supplier_pricing_review | 2 | LOW |
| sf_supplier_pricing_tiers | 2 | LOW |
| sf_supplier_questionnaire | 2 | LOW |
| sf_supplier_risk_dashboard | 2 | LOW |
| sf_supplier_risk_mitigation | 2 | LOW |
| sf_supplier_risk_mitigation_plan | 2 | LOW |
| sf_supplier_risk_register | 2 | LOW |
| sf_supplier_risk_score | 2 | LOW |
| sf_supplier_scorecard_review | 2 | LOW |
| sf_system_health_check | 2 | LOW |
| sf_tax_deadline_calendar | 2 | LOW |
| sf_tax_provision_calc | 2 | LOW |
| sf_telework_policy | 2 | LOW |
| sf_territory_mapping | 2 | LOW |
| sf_third_party_risk | 2 | LOW |
| sf_tooling_request | 2 | LOW |
| sf_training_budget | 2 | LOW |
| sf_training_feedback | 2 | LOW |
| sf_treasury_week_board | 2 | LOW |
| sf_upsell_trigger_rules | 2 | LOW |
| sf_user_activity_log | 2 | LOW |
| sf_vendor_sample_tracking | 2 | LOW |
| sf_vendor_scorecard_auto | 2 | LOW |
| sf_vendor_sla_monitor | 2 | LOW |
| sf_warehouse_layout_planner | 2 | LOW |
| sf_warehouse_safety_log | 2 | LOW |
| sf_warehouse_slotting_review | 2 | LOW |
| sf_warehouse_throughput | 2 | LOW |
| sf_warehouse_throughput_daily | 2 | LOW |
| sf_warning_letter_register | 2 | LOW |
| sf_warranty_cost_analytics | 2 | LOW |
| sf_waste_stream_tracker | 2 | LOW |
| sf_win_loss_analysis | 2 | LOW |
| sf_workorder_handover | 2 | LOW |
| sf_zone_capacity_monitor | 2 | LOW |

## Issues by Type

### Manifest Version
**Description:** Manifest version 18.x -> 19.x

**Fix:** Change 'version': '18.0.x.x' to '19.0.x.x'

**Modules affected:** 358

| Module | Occurrences |
|--------|-------------|
| sf_access_request_workflow | 2 |
| sf_accrual_proposals | 2 |
| sf_accrual_reversal_auto | 2 |
| sf_anniversary_reminders | 2 |
| sf_api_integration_log | 2 |
| sf_asset_count_campaign | 2 |
| sf_asset_disposal_request | 2 |
| sf_backup_verification_log | 2 |
| sf_bank_fee_analytics | 2 |
| sf_bank_reconciliation_rules | 2 |
| sf_batch_job_monitor | 2 |
| sf_blanket_order_release | 2 |
| sf_bom_change_request | 2 |
| sf_budget_virement | 2 |
| sf_budget_vs_actual_alerts | 2 |
| sf_business_glossary | 2 |
| sf_business_requirement | 2 |
| sf_capacity_forecast_sales | 2 |
| sf_capacity_planner | 2 |
| sf_capital_expenditure_plan | 2 |
| sf_carrier_performance | 2 |
| sf_certificate_requests | 2 |
| sf_change_freeze_calendar | 2 |
| sf_checklist_library | 2 |
| sf_churn_prediction_rules | 2 |
| sf_commission_clawback | 2 |
| sf_committee_decisions | 2 |
| sf_company_car_policy | 2 |
| sf_compensation_benchmark | 2 |
| sf_competitive_intel_register | 2 |
| sf_compliance_calendar | 2 |
| sf_compliance_obligation | 2 |
| sf_contract_compliance_audit | 2 |
| sf_credit_note_reasons | 2 |
| sf_cross_sell_engine | 2 |
| sf_crossdock_operations | 2 |
| sf_currency_exposure_map | 2 |
| sf_customer_advisory_board | 2 |
| sf_customer_advocacy_program | 2 |
| sf_customer_care_coaching | 2 |
| sf_customer_care_coaching_plan | 2 |
| sf_customer_care_escalation | 2 |
| sf_customer_care_escalation_dashboard | 2 |
| sf_customer_care_escalation_matrix | 2 |
| sf_customer_care_escalation_rules | 2 |
| sf_customer_care_escalation_tracker | 2 |
| sf_customer_care_journey | 2 |
| sf_customer_care_program | 2 |
| sf_customer_care_qa_review | 2 |
| sf_customer_care_qa_scorecard | 2 |
| sf_customer_care_satisfaction | 2 |
| sf_customer_care_satisfaction_survey | 2 |
| sf_customer_care_sla | 2 |
| sf_customer_care_sla_breach | 2 |
| sf_customer_care_sla_dashboard | 2 |
| sf_customer_care_sla_rules | 2 |
| sf_customer_care_survey | 2 |
| sf_customer_care_training | 2 |
| sf_customer_care_training_plan | 2 |
| sf_customer_care_workforce | 2 |
| sf_customer_care_workforce_plan | 2 |
| sf_customer_care_workload | 2 |
| sf_customer_churn_analytics | 2 |
| sf_customer_complaint_praise | 2 |
| sf_customer_contract_renewal_forecast | 2 |
| sf_customer_contract_renewal_pipeline | 2 |
| sf_customer_covenant_tracker | 2 |
| sf_customer_document_vault | 2 |
| sf_customer_escalation_matrix | 2 |
| sf_customer_expansion_tracker | 2 |
| sf_customer_feedback_actions | 2 |
| sf_customer_feedback_analytics | 2 |
| sf_customer_health_scoring | 2 |
| sf_customer_incident_comms | 2 |
| sf_customer_journey_analytics | 2 |
| sf_customer_journey_map | 2 |
| sf_customer_journey_mapper | 2 |
| sf_customer_journey_stage | 2 |
| sf_customer_onboarding_checklist | 2 |
| sf_customer_onboarding_cost | 2 |
| sf_customer_onboarding_docs | 2 |
| sf_customer_pain_point | 2 |
| sf_customer_payment_behavior | 2 |
| sf_customer_payment_plan | 2 |
| sf_customer_portal_tasks | 2 |
| sf_customer_pricing_requests | 2 |
| sf_customer_priority_matrix | 2 |
| sf_customer_profitability_rank | 2 |
| sf_customer_reference_program | 2 |
| sf_customer_reference_tracker | 2 |
| sf_customer_revenue_trend | 2 |
| sf_customer_risk_score | 2 |
| sf_customer_satisfaction_trend | 2 |
| sf_customer_segment_rules | 2 |
| sf_customer_segments_rules | 2 |
| sf_customer_visit_reports | 2 |
| sf_cycle_count_scheduler | 2 |
| sf_damaged_goods_log | 2 |
| sf_data_quality_check | 2 |
| sf_deal_desk_request | 2 |
| sf_decision_log | 2 |
| sf_demand_planning_review | 2 |
| sf_disciplinary_action | 2 |
| sf_dividend_register | 2 |
| sf_document_approval_hybrid | 2 |
| sf_dr_plan_tracker | 2 |
| sf_dropship_operations | 2 |
| sf_ehs_inspection_schedule | 2 |
| sf_emergency_purchase_log | 2 |
| sf_employee_1on1_tracker | 2 |
| sf_employee_asset_return | 2 |
| sf_employee_engagement_action | 2 |
| sf_employee_referral | 2 |
| sf_employee_skill_gap | 2 |
| sf_employee_survey | 2 |
| sf_energy_meter_readings | 2 |
| sf_energy_saving_tracker | 2 |
| sf_environmental_waste_tracking | 2 |
| sf_equipment_utilization | 2 |
| sf_exit_interviews | 2 |
| sf_expiry_alert_manager | 2 |
| sf_external_audit_tracker | 2 |
| sf_field_service_checklist | 2 |
| sf_field_service_customer_satisfaction | 2 |
| sf_field_service_dispatch | 2 |
| sf_field_service_parts | 2 |
| sf_financial_covenant_monitor | 2 |
| sf_financial_ratio_dashboard | 2 |
| sf_first_piece_validation | 2 |
| sf_fixed_asset_transfer | 2 |
| sf_freight_quote_compare | 2 |
| sf_fx_hedge_accounting | 2 |
| sf_fx_reval_scheduler | 2 |
| sf_grievance_tracker | 2 |
| sf_incident_oncall | 2 |
| sf_intercompany_balance_check | 2 |
| sf_intercompany_loan | 2 |
| sf_interim_billing_tracker | 2 |
| sf_internal_audit_program | 2 |
| sf_internal_mobility | 2 |
| sf_internship_tracker | 2 |
| sf_inventory_abc_classification | 2 |
| sf_inventory_accuracy_rate | 2 |
| sf_inventory_count_variance | 2 |
| sf_inventory_revaluation | 2 |
| sf_inventory_shrinkage_tracker | 2 |
| sf_inventory_turnover_analysis | 2 |
| sf_inventory_writeoff_register | 2 |
| sf_invoice_discounting | 2 |
| sf_it_asset_lifecycle | 2 |
| sf_it_capacity_planning | 2 |
| sf_job_costing_snapshot | 2 |
| sf_key_account_plans | 2 |
| sf_knowledge_articles | 2 |
| sf_kpi_target_register | 2 |
| sf_late_payment_interest | 2 |
| sf_line_balancing_review | 2 |
| sf_maintenance_cost_tracker | 2 |
| sf_maintenance_intake | 2 |
| sf_maintenance_schedule_optimizer | 2 |
| sf_marketing_budget_tracker | 2 |
| sf_marketing_campaign_roi | 2 |
| sf_meeting_minutes | 2 |
| sf_mgmt_fee_billing | 2 |
| sf_min_order_enforcement | 2 |
| sf_minmax_review | 2 |
| sf_multi_site_price_harmony | 2 |
| sf_nonconformance_cost | 2 |
| sf_obsolescence_forecast | 2 |
| sf_onboarding_cost | 2 |
| sf_oncall_schedule | 2 |
| sf_ooo_calendar | 2 |
| sf_operator_skill_matrix | 2 |
| sf_order_freeze_windows | 2 |
| sf_overtime_preapproval | 2 |
| sf_packaging_spec_register | 2 |
| sf_pallet_sscc_labels | 2 |
| sf_payment_milestone_engine | 2 |
| sf_payroll_deadline_tracker | 2 |
| sf_peak_season_planning | 2 |
| sf_po_acknowledgment | 2 |
| sf_po_amendment_log | 2 |
| sf_po_budget_check | 2 |
| sf_policy_exception_tracker | 2 |
| sf_prepaid_amortization | 2 |
| sf_probation_review_tracker | 2 |
| sf_procurement_savings_tracker | 2 |
| sf_product_lifecycle_stage | 2 |
| sf_product_margin_matrix | 2 |
| sf_product_return_rate | 2 |
| sf_product_return_reasons | 2 |
| sf_production_capacity_plan | 2 |
| sf_production_capacity_review | 2 |
| sf_production_capacity_whatif | 2 |
| sf_production_downtime_pareto | 2 |
| sf_production_line_efficiency | 2 |
| sf_production_meeting_actions | 2 |
| sf_production_oee_calculator | 2 |
| sf_production_oee_dashboard | 2 |
| sf_production_oee_tracker | 2 |
| sf_production_order_priority | 2 |
| sf_production_order_sequencing | 2 |
| sf_production_scenarios | 2 |
| sf_production_schedule_alert | 2 |
| sf_production_scrap_analytics | 2 |
| sf_production_scrap_pareto | 2 |
| sf_production_trial_tracking | 2 |
| sf_production_waste_tracker | 2 |
| sf_production_yield_analysis | 2 |
| sf_production_yield_tracker | 2 |
| sf_project_change_request | 2 |
| sf_project_charter | 2 |
| sf_project_lessons_learned | 2 |
| sf_project_milestone_tracker | 2 |
| sf_project_portfolio_board | 2 |
| sf_project_resource_plan | 2 |
| sf_project_risk_log | 2 |
| sf_project_stakeholder | 2 |
| sf_provision_register | 2 |
| sf_purchase_approval_matrix | 2 |
| sf_purchase_contract_compliance | 2 |
| sf_purchase_envelope | 2 |
| sf_purchase_order_aging | 2 |
| sf_purchase_requisition_analytics | 2 |
| sf_purchase_requisition_template | 2 |
| sf_quality_alert_aging | 2 |
| sf_quality_alert_auto_assign | 2 |
| sf_quality_alert_escalation | 2 |
| sf_quality_audit_program | 2 |
| sf_quality_cost_tracker | 2 |
| sf_quality_document_control | 2 |
| sf_quality_document_control_sys | 2 |
| sf_quality_hold_register | 2 |
| sf_quality_inspection_mobile2 | 2 |
| sf_quality_inspection_plan | 2 |
| sf_quality_inspection_planner | 2 |
| sf_quality_pareto_analyzer | 2 |
| sf_quality_pareto_update | 2 |
| sf_quality_trend_dashboard | 2 |
| sf_quote_followup_cadence | 2 |
| sf_receiving_discrepancy_log | 2 |
| sf_recurring_cost_register | 2 |
| sf_recurring_revenue_register | 2 |
| sf_recurring_task_templates | 2 |
| sf_regulatory_watch | 2 |
| sf_remote_work_requests | 2 |
| sf_replenishment_review | 2 |
| sf_retention_schedule | 2 |
| sf_revenue_backlog_tracker | 2 |
| sf_revenue_leak_detector | 2 |
| sf_revenue_leakage_analyzer | 2 |
| sf_revenue_milestone | 2 |
| sf_revenue_protection_plan | 2 |
| sf_runbook_library | 2 |
| sf_safety_inspections | 2 |
| sf_safety_training_tracker | 2 |
| sf_sales_asset_library | 2 |
| sf_sales_battle_rhythm | 2 |
| sf_sales_battlecard | 2 |
| sf_sales_capacity_model | 2 |
| sf_sales_coaching_dashboard | 2 |
| sf_sales_coaching_effectiveness | 2 |
| sf_sales_coaching_log | 2 |
| sf_sales_coaching_plan | 2 |
| sf_sales_commission_plan | 2 |
| sf_sales_commission_simulation | 2 |
| sf_sales_commission_statement | 2 |
| sf_sales_content_library | 2 |
| sf_sales_enablement_tracker | 2 |
| sf_sales_forecast_accuracy | 2 |
| sf_sales_forecast_category | 2 |
| sf_sales_gamification | 2 |
| sf_sales_hiring_funnel | 2 |
| sf_sales_hiring_plan | 2 |
| sf_sales_hiring_tracker | 2 |
| sf_sales_huddle_notes | 2 |
| sf_sales_hygiene_audit | 2 |
| sf_sales_onboarding_plan | 2 |
| sf_sales_order_acknowledgment | 2 |
| sf_sales_pipeline_review | 2 |
| sf_sales_play_execution | 2 |
| sf_sales_playbook | 2 |
| sf_sales_target_cascade | 2 |
| sf_sales_territory_planner | 2 |
| sf_sales_territory_review | 2 |
| sf_scrap_reason_analytics | 2 |
| sf_sell_through_reporting | 2 |
| sf_service_catalog | 2 |
| sf_service_level_agreement_monitor | 2 |
| sf_shift_swap_board | 2 |
| sf_sla_pause_tracking | 2 |
| sf_software_license_renewals | 2 |
| sf_spare_parts_minmax | 2 |
| sf_special_price_approval | 2 |
| sf_stock_adjustment_approval | 2 |
| sf_succession_plan | 2 |
| sf_supplier_audit_program | 2 |
| sf_supplier_audit_scheduler | 2 |
| sf_supplier_bank_change_alert | 2 |
| sf_supplier_capacity_check | 2 |
| sf_supplier_capacity_forecast | 2 |
| sf_supplier_capacity_planner | 2 |
| sf_supplier_capacity_review | 2 |
| sf_supplier_contract_database | 2 |
| sf_supplier_contract_renewal | 2 |
| sf_supplier_contract_renewal_alert | 2 |
| sf_supplier_contract_renewal_tracker | 2 |
| sf_supplier_diversity_tracker | 2 |
| sf_supplier_invoice_3way_match | 2 |
| sf_supplier_invoice_3way_match3 | 2 |
| sf_supplier_invoice_accuracy | 2 |
| sf_supplier_invoice_matching | 2 |
| sf_supplier_leadtime_audit | 2 |
| sf_supplier_negotiation_prep | 2 |
| sf_supplier_onboarding_checklist | 2 |
| sf_supplier_onboarding_portal | 2 |
| sf_supplier_pareto_abc | 2 |
| sf_supplier_payment_optimization | 2 |
| sf_supplier_payment_terms | 2 |
| sf_supplier_performance_dashboard | 2 |
| sf_supplier_performance_review | 2 |
| sf_supplier_pricing_benchmark | 2 |
| sf_supplier_pricing_history | 2 |
| sf_supplier_pricing_review | 2 |
| sf_supplier_pricing_tiers | 2 |
| sf_supplier_questionnaire | 2 |
| sf_supplier_risk_dashboard | 2 |
| sf_supplier_risk_mitigation | 2 |
| sf_supplier_risk_mitigation_plan | 2 |
| sf_supplier_risk_register | 2 |
| sf_supplier_risk_score | 2 |
| sf_supplier_scorecard_review | 2 |
| sf_system_health_check | 2 |
| sf_tax_deadline_calendar | 2 |
| sf_tax_provision_calc | 2 |
| sf_telework_policy | 2 |
| sf_territory_mapping | 2 |
| sf_third_party_risk | 2 |
| sf_tooling_request | 2 |
| sf_training_budget | 2 |
| sf_training_feedback | 2 |
| sf_treasury_week_board | 2 |
| sf_upsell_trigger_rules | 2 |
| sf_user_activity_log | 2 |
| sf_vendor_sample_tracking | 2 |
| sf_vendor_scorecard_auto | 2 |
| sf_vendor_sla_monitor | 2 |
| sf_warehouse_layout_planner | 2 |
| sf_warehouse_safety_log | 2 |
| sf_warehouse_slotting_review | 2 |
| sf_warehouse_throughput | 2 |
| sf_warehouse_throughput_daily | 2 |
| sf_warning_letter_register | 2 |
| sf_warranty_cost_analytics | 2 |
| sf_waste_stream_tracker | 2 |
| sf_win_loss_analysis | 2 |
| sf_workorder_handover | 2 |
| sf_zone_capacity_monitor | 2 |

## Manifest Version Updates Required

| Module | Current Version Line |
|--------|---------------------|
| sf_access_request_workflow | 'version': '18.0.1.0.0', |
| sf_accrual_proposals | 'version': '18.0.1.0.0', |
| sf_accrual_reversal_auto | 'version': '18.0.1.0.0', |
| sf_anniversary_reminders | 'version': '18.0.1.0.0', |
| sf_api_integration_log | 'version': '18.0.1.0.0', |
| sf_asset_count_campaign | 'version': '18.0.1.0.0', |
| sf_asset_disposal_request | 'version': '18.0.1.0.0', |
| sf_backup_verification_log | 'version': '18.0.1.0.0', |
| sf_bank_fee_analytics | 'version': '18.0.1.0.0', |
| sf_bank_reconciliation_rules | 'version': '18.0.1.0.0', |
| sf_batch_job_monitor | 'version': '18.0.1.0.0', |
| sf_blanket_order_release | 'version': '18.0.1.0.0', |
| sf_bom_change_request | 'version': '18.0.1.0.0', |
| sf_budget_virement | 'version': '18.0.1.0.0', |
| sf_budget_vs_actual_alerts | 'version': '18.0.1.0.0', |
| sf_business_glossary | 'version': '18.0.1.0.0', |
| sf_business_requirement | 'version': '18.0.1.0.0', |
| sf_capacity_forecast_sales | 'version': '18.0.1.0.0', |
| sf_capacity_planner | 'version': '18.0.1.0.0', |
| sf_capital_expenditure_plan | 'version': '18.0.1.0.0', |
| sf_carrier_performance | 'version': '18.0.1.0.0', |
| sf_certificate_requests | 'version': '18.0.1.0.0', |
| sf_change_freeze_calendar | 'version': '18.0.1.0.0', |
| sf_checklist_library | 'version': '18.0.1.0.0', |
| sf_churn_prediction_rules | 'version': '18.0.1.0.0', |
| sf_commission_clawback | 'version': '18.0.1.0.0', |
| sf_committee_decisions | 'version': '18.0.1.0.0', |
| sf_company_car_policy | 'version': '18.0.1.0.0', |
| sf_compensation_benchmark | 'version': '18.0.1.0.0', |
| sf_competitive_intel_register | 'version': '18.0.1.0.0', |
| sf_compliance_calendar | 'version': '18.0.1.0.0', |
| sf_compliance_obligation | 'version': '18.0.1.0.0', |
| sf_contract_compliance_audit | 'version': '18.0.1.0.0', |
| sf_credit_note_reasons | 'version': '18.0.1.0.0', |
| sf_cross_sell_engine | 'version': '18.0.1.0.0', |
| sf_crossdock_operations | 'version': '18.0.1.0.0', |
| sf_currency_exposure_map | 'version': '18.0.1.0.0', |
| sf_customer_advisory_board | 'version': '18.0.1.0.0', |
| sf_customer_advocacy_program | 'version': '18.0.1.0.0', |
| sf_customer_care_coaching | 'version': '18.0.1.0.0', |
| sf_customer_care_coaching_plan | 'version': '18.0.1.0.0', |
| sf_customer_care_escalation | 'version': '18.0.1.0.0', |
| sf_customer_care_escalation_dashboard | 'version': '18.0.1.0.0', |
| sf_customer_care_escalation_matrix | 'version': '18.0.1.0.0', |
| sf_customer_care_escalation_rules | 'version': '18.0.1.0.0', |
| sf_customer_care_escalation_tracker | 'version': '18.0.1.0.0', |
| sf_customer_care_journey | 'version': '18.0.1.0.0', |
| sf_customer_care_program | 'version': '18.0.1.0.0', |
| sf_customer_care_qa_review | 'version': '18.0.1.0.0', |
| sf_customer_care_qa_scorecard | 'version': '18.0.1.0.0', |
| sf_customer_care_satisfaction | 'version': '18.0.1.0.0', |
| sf_customer_care_satisfaction_survey | 'version': '18.0.1.0.0', |
| sf_customer_care_sla | 'version': '18.0.1.0.0', |
| sf_customer_care_sla_breach | 'version': '18.0.1.0.0', |
| sf_customer_care_sla_dashboard | 'version': '18.0.1.0.0', |
| sf_customer_care_sla_rules | 'version': '18.0.1.0.0', |
| sf_customer_care_survey | 'version': '18.0.1.0.0', |
| sf_customer_care_training | 'version': '18.0.1.0.0', |
| sf_customer_care_training_plan | 'version': '18.0.1.0.0', |
| sf_customer_care_workforce | 'version': '18.0.1.0.0', |
| sf_customer_care_workforce_plan | 'version': '18.0.1.0.0', |
| sf_customer_care_workload | 'version': '18.0.1.0.0', |
| sf_customer_churn_analytics | 'version': '18.0.1.0.0', |
| sf_customer_complaint_praise | 'version': '18.0.1.0.0', |
| sf_customer_contract_renewal_forecast | 'version': '18.0.1.0.0', |
| sf_customer_contract_renewal_pipeline | 'version': '18.0.1.0.0', |
| sf_customer_covenant_tracker | 'version': '18.0.1.0.0', |
| sf_customer_document_vault | 'version': '18.0.1.0.0', |
| sf_customer_escalation_matrix | 'version': '18.0.1.0.0', |
| sf_customer_expansion_tracker | 'version': '18.0.1.0.0', |
| sf_customer_feedback_actions | 'version': '18.0.1.0.0', |
| sf_customer_feedback_analytics | 'version': '18.0.1.0.0', |
| sf_customer_health_scoring | 'version': '18.0.1.0.0', |
| sf_customer_incident_comms | 'version': '18.0.1.0.0', |
| sf_customer_journey_analytics | 'version': '18.0.1.0.0', |
| sf_customer_journey_map | 'version': '18.0.1.0.0', |
| sf_customer_journey_mapper | 'version': '18.0.1.0.0', |
| sf_customer_journey_stage | 'version': '18.0.1.0.0', |
| sf_customer_onboarding_checklist | 'version': '18.0.1.0.0', |
| sf_customer_onboarding_cost | 'version': '18.0.1.0.0', |
| sf_customer_onboarding_docs | 'version': '18.0.1.0.0', |
| sf_customer_pain_point | 'version': '18.0.1.0.0', |
| sf_customer_payment_behavior | 'version': '18.0.1.0.0', |
| sf_customer_payment_plan | 'version': '18.0.1.0.0', |
| sf_customer_portal_tasks | 'version': '18.0.1.0.0', |
| sf_customer_pricing_requests | 'version': '18.0.1.0.0', |
| sf_customer_priority_matrix | 'version': '18.0.1.0.0', |
| sf_customer_profitability_rank | 'version': '18.0.1.0.0', |
| sf_customer_reference_program | 'version': '18.0.1.0.0', |
| sf_customer_reference_tracker | 'version': '18.0.1.0.0', |
| sf_customer_revenue_trend | 'version': '18.0.1.0.0', |
| sf_customer_risk_score | 'version': '18.0.1.0.0', |
| sf_customer_satisfaction_trend | 'version': '18.0.1.0.0', |
| sf_customer_segment_rules | 'version': '18.0.1.0.0', |
| sf_customer_segments_rules | 'version': '18.0.1.0.0', |
| sf_customer_visit_reports | 'version': '18.0.1.0.0', |
| sf_cycle_count_scheduler | 'version': '18.0.1.0.0', |
| sf_damaged_goods_log | 'version': '18.0.1.0.0', |
| sf_data_quality_check | 'version': '18.0.1.0.0', |
| sf_deal_desk_request | 'version': '18.0.1.0.0', |
| sf_decision_log | 'version': '18.0.1.0.0', |
| sf_demand_planning_review | 'version': '18.0.1.0.0', |
| sf_disciplinary_action | 'version': '18.0.1.0.0', |
| sf_dividend_register | 'version': '18.0.1.0.0', |
| sf_document_approval_hybrid | 'version': '18.0.1.0.0', |
| sf_dr_plan_tracker | 'version': '18.0.1.0.0', |
| sf_dropship_operations | 'version': '18.0.1.0.0', |
| sf_ehs_inspection_schedule | 'version': '18.0.1.0.0', |
| sf_emergency_purchase_log | 'version': '18.0.1.0.0', |
| sf_employee_1on1_tracker | 'version': '18.0.1.0.0', |
| sf_employee_asset_return | 'version': '18.0.1.0.0', |
| sf_employee_engagement_action | 'version': '18.0.1.0.0', |
| sf_employee_referral | 'version': '18.0.1.0.0', |
| sf_employee_skill_gap | 'version': '18.0.1.0.0', |
| sf_employee_survey | 'version': '18.0.1.0.0', |
| sf_energy_meter_readings | 'version': '18.0.1.0.0', |
| sf_energy_saving_tracker | 'version': '18.0.1.0.0', |
| sf_environmental_waste_tracking | 'version': '18.0.1.0.0', |
| sf_equipment_utilization | 'version': '18.0.1.0.0', |
| sf_exit_interviews | 'version': '18.0.1.0.0', |
| sf_expiry_alert_manager | 'version': '18.0.1.0.0', |
| sf_external_audit_tracker | 'version': '18.0.1.0.0', |
| sf_field_service_checklist | 'version': '18.0.1.0.0', |
| sf_field_service_customer_satisfaction | 'version': '18.0.1.0.0', |
| sf_field_service_dispatch | 'version': '18.0.1.0.0', |
| sf_field_service_parts | 'version': '18.0.1.0.0', |
| sf_financial_covenant_monitor | 'version': '18.0.1.0.0', |
| sf_financial_ratio_dashboard | 'version': '18.0.1.0.0', |
| sf_first_piece_validation | 'version': '18.0.1.0.0', |
| sf_fixed_asset_transfer | 'version': '18.0.1.0.0', |
| sf_freight_quote_compare | 'version': '18.0.1.0.0', |
| sf_fx_hedge_accounting | 'version': '18.0.1.0.0', |
| sf_fx_reval_scheduler | 'version': '18.0.1.0.0', |
| sf_grievance_tracker | 'version': '18.0.1.0.0', |
| sf_incident_oncall | 'version': '18.0.1.0.0', |
| sf_intercompany_balance_check | 'version': '18.0.1.0.0', |
| sf_intercompany_loan | 'version': '18.0.1.0.0', |
| sf_interim_billing_tracker | 'version': '18.0.1.0.0', |
| sf_internal_audit_program | 'version': '18.0.1.0.0', |
| sf_internal_mobility | 'version': '18.0.1.0.0', |
| sf_internship_tracker | 'version': '18.0.1.0.0', |
| sf_inventory_abc_classification | 'version': '18.0.1.0.0', |
| sf_inventory_accuracy_rate | 'version': '18.0.1.0.0', |
| sf_inventory_count_variance | 'version': '18.0.1.0.0', |
| sf_inventory_revaluation | 'version': '18.0.1.0.0', |
| sf_inventory_shrinkage_tracker | 'version': '18.0.1.0.0', |
| sf_inventory_turnover_analysis | 'version': '18.0.1.0.0', |
| sf_inventory_writeoff_register | 'version': '18.0.1.0.0', |
| sf_invoice_discounting | 'version': '18.0.1.0.0', |
| sf_it_asset_lifecycle | 'version': '18.0.1.0.0', |
| sf_it_capacity_planning | 'version': '18.0.1.0.0', |
| sf_job_costing_snapshot | 'version': '18.0.1.0.0', |
| sf_key_account_plans | 'version': '18.0.1.0.0', |
| sf_knowledge_articles | 'version': '18.0.1.0.0', |
| sf_kpi_target_register | 'version': '18.0.1.0.0', |
| sf_late_payment_interest | 'version': '18.0.1.0.0', |
| sf_line_balancing_review | 'version': '18.0.1.0.0', |
| sf_maintenance_cost_tracker | 'version': '18.0.1.0.0', |
| sf_maintenance_intake | 'version': '18.0.1.0.0', |
| sf_maintenance_schedule_optimizer | 'version': '18.0.1.0.0', |
| sf_marketing_budget_tracker | 'version': '18.0.1.0.0', |
| sf_marketing_campaign_roi | 'version': '18.0.1.0.0', |
| sf_meeting_minutes | 'version': '18.0.1.0.0', |
| sf_mgmt_fee_billing | 'version': '18.0.1.0.0', |
| sf_min_order_enforcement | 'version': '18.0.1.0.0', |
| sf_minmax_review | 'version': '18.0.1.0.0', |
| sf_multi_site_price_harmony | 'version': '18.0.1.0.0', |
| sf_nonconformance_cost | 'version': '18.0.1.0.0', |
| sf_obsolescence_forecast | 'version': '18.0.1.0.0', |
| sf_onboarding_cost | 'version': '18.0.1.0.0', |
| sf_oncall_schedule | 'version': '18.0.1.0.0', |
| sf_ooo_calendar | 'version': '18.0.1.0.0', |
| sf_operator_skill_matrix | 'version': '18.0.1.0.0', |
| sf_order_freeze_windows | 'version': '18.0.1.0.0', |
| sf_overtime_preapproval | 'version': '18.0.1.0.0', |
| sf_packaging_spec_register | 'version': '18.0.1.0.0', |
| sf_pallet_sscc_labels | 'version': '18.0.1.0.0', |
| sf_payment_milestone_engine | 'version': '18.0.1.0.0', |
| sf_payroll_deadline_tracker | 'version': '18.0.1.0.0', |
| sf_peak_season_planning | 'version': '18.0.1.0.0', |
| sf_po_acknowledgment | 'version': '18.0.1.0.0', |
| sf_po_amendment_log | 'version': '18.0.1.0.0', |
| sf_po_budget_check | 'version': '18.0.1.0.0', |
| sf_policy_exception_tracker | 'version': '18.0.1.0.0', |
| sf_prepaid_amortization | 'version': '18.0.1.0.0', |
| sf_probation_review_tracker | 'version': '18.0.1.0.0', |
| sf_procurement_savings_tracker | 'version': '18.0.1.0.0', |
| sf_product_lifecycle_stage | 'version': '18.0.1.0.0', |
| sf_product_margin_matrix | 'version': '18.0.1.0.0', |
| sf_product_return_rate | 'version': '18.0.1.0.0', |
| sf_product_return_reasons | 'version': '18.0.1.0.0', |
| sf_production_capacity_plan | 'version': '18.0.1.0.0', |
| sf_production_capacity_review | 'version': '18.0.1.0.0', |
| sf_production_capacity_whatif | 'version': '18.0.1.0.0', |
| sf_production_downtime_pareto | 'version': '18.0.1.0.0', |
| sf_production_line_efficiency | 'version': '18.0.1.0.0', |
| sf_production_meeting_actions | 'version': '18.0.1.0.0', |
| sf_production_oee_calculator | 'version': '18.0.1.0.0', |
| sf_production_oee_dashboard | 'version': '18.0.1.0.0', |
| sf_production_oee_tracker | 'version': '18.0.1.0.0', |
| sf_production_order_priority | 'version': '18.0.1.0.0', |
| sf_production_order_sequencing | 'version': '18.0.1.0.0', |
| sf_production_scenarios | 'version': '18.0.1.0.0', |
| sf_production_schedule_alert | 'version': '18.0.1.0.0', |
| sf_production_scrap_analytics | 'version': '18.0.1.0.0', |
| sf_production_scrap_pareto | 'version': '18.0.1.0.0', |
| sf_production_trial_tracking | 'version': '18.0.1.0.0', |
| sf_production_waste_tracker | 'version': '18.0.1.0.0', |
| sf_production_yield_analysis | 'version': '18.0.1.0.0', |
| sf_production_yield_tracker | 'version': '18.0.1.0.0', |
| sf_project_change_request | 'version': '18.0.1.0.0', |
| sf_project_charter | 'version': '18.0.1.0.0', |
| sf_project_lessons_learned | 'version': '18.0.1.0.0', |
| sf_project_milestone_tracker | 'version': '18.0.1.0.0', |
| sf_project_portfolio_board | 'version': '18.0.1.0.0', |
| sf_project_resource_plan | 'version': '18.0.1.0.0', |
| sf_project_risk_log | 'version': '18.0.1.0.0', |
| sf_project_stakeholder | 'version': '18.0.1.0.0', |
| sf_provision_register | 'version': '18.0.1.0.0', |
| sf_purchase_approval_matrix | 'version': '18.0.1.0.0', |
| sf_purchase_contract_compliance | 'version': '18.0.1.0.0', |
| sf_purchase_envelope | 'version': '18.0.1.0.0', |
| sf_purchase_order_aging | 'version': '18.0.1.0.0', |
| sf_purchase_requisition_analytics | 'version': '18.0.1.0.0', |
| sf_purchase_requisition_template | 'version': '18.0.1.0.0', |
| sf_quality_alert_aging | 'version': '18.0.1.0.0', |
| sf_quality_alert_auto_assign | 'version': '18.0.1.0.0', |
| sf_quality_alert_escalation | 'version': '18.0.1.0.0', |
| sf_quality_audit_program | 'version': '18.0.1.0.0', |
| sf_quality_cost_tracker | 'version': '18.0.1.0.0', |
| sf_quality_document_control | 'version': '18.0.1.0.0', |
| sf_quality_document_control_sys | 'version': '18.0.1.0.0', |
| sf_quality_hold_register | 'version': '18.0.1.0.0', |
| sf_quality_inspection_mobile2 | 'version': '18.0.1.0.0', |
| sf_quality_inspection_plan | 'version': '18.0.1.0.0', |
| sf_quality_inspection_planner | 'version': '18.0.1.0.0', |
| sf_quality_pareto_analyzer | 'version': '18.0.1.0.0', |
| sf_quality_pareto_update | 'version': '18.0.1.0.0', |
| sf_quality_trend_dashboard | 'version': '18.0.1.0.0', |
| sf_quote_followup_cadence | 'version': '18.0.1.0.0', |
| sf_receiving_discrepancy_log | 'version': '18.0.1.0.0', |
| sf_recurring_cost_register | 'version': '18.0.1.0.0', |
| sf_recurring_revenue_register | 'version': '18.0.1.0.0', |
| sf_recurring_task_templates | 'version': '18.0.1.0.0', |
| sf_regulatory_watch | 'version': '18.0.1.0.0', |
| sf_remote_work_requests | 'version': '18.0.1.0.0', |
| sf_replenishment_review | 'version': '18.0.1.0.0', |
| sf_retention_schedule | 'version': '18.0.1.0.0', |
| sf_revenue_backlog_tracker | 'version': '18.0.1.0.0', |
| sf_revenue_leak_detector | 'version': '18.0.1.0.0', |
| sf_revenue_leakage_analyzer | 'version': '18.0.1.0.0', |
| sf_revenue_milestone | 'version': '18.0.1.0.0', |
| sf_revenue_protection_plan | 'version': '18.0.1.0.0', |
| sf_runbook_library | 'version': '18.0.1.0.0', |
| sf_safety_inspections | 'version': '18.0.1.0.0', |
| sf_safety_training_tracker | 'version': '18.0.1.0.0', |
| sf_sales_asset_library | 'version': '18.0.1.0.0', |
| sf_sales_battle_rhythm | 'version': '18.0.1.0.0', |
| sf_sales_battlecard | 'version': '18.0.1.0.0', |
| sf_sales_capacity_model | 'version': '18.0.1.0.0', |
| sf_sales_coaching_dashboard | 'version': '18.0.1.0.0', |
| sf_sales_coaching_effectiveness | 'version': '18.0.1.0.0', |
| sf_sales_coaching_log | 'version': '18.0.1.0.0', |
| sf_sales_coaching_plan | 'version': '18.0.1.0.0', |
| sf_sales_commission_plan | 'version': '18.0.1.0.0', |
| sf_sales_commission_simulation | 'version': '18.0.1.0.0', |
| sf_sales_commission_statement | 'version': '18.0.1.0.0', |
| sf_sales_content_library | 'version': '18.0.1.0.0', |
| sf_sales_enablement_tracker | 'version': '18.0.1.0.0', |
| sf_sales_forecast_accuracy | 'version': '18.0.1.0.0', |
| sf_sales_forecast_category | 'version': '18.0.1.0.0', |
| sf_sales_gamification | 'version': '18.0.1.0.0', |
| sf_sales_hiring_funnel | 'version': '18.0.1.0.0', |
| sf_sales_hiring_plan | 'version': '18.0.1.0.0', |
| sf_sales_hiring_tracker | 'version': '18.0.1.0.0', |
| sf_sales_huddle_notes | 'version': '18.0.1.0.0', |
| sf_sales_hygiene_audit | 'version': '18.0.1.0.0', |
| sf_sales_onboarding_plan | 'version': '18.0.1.0.0', |
| sf_sales_order_acknowledgment | 'version': '18.0.1.0.0', |
| sf_sales_pipeline_review | 'version': '18.0.1.0.0', |
| sf_sales_play_execution | 'version': '18.0.1.0.0', |
| sf_sales_playbook | 'version': '18.0.1.0.0', |
| sf_sales_target_cascade | 'version': '18.0.1.0.0', |
| sf_sales_territory_planner | 'version': '18.0.1.0.0', |
| sf_sales_territory_review | 'version': '18.0.1.0.0', |
| sf_scrap_reason_analytics | 'version': '18.0.1.0.0', |
| sf_sell_through_reporting | 'version': '18.0.1.0.0', |
| sf_service_catalog | 'version': '18.0.1.0.0', |
| sf_service_level_agreement_monitor | 'version': '18.0.1.0.0', |
| sf_shift_swap_board | 'version': '18.0.1.0.0', |
| sf_sla_pause_tracking | 'version': '18.0.1.0.0', |
| sf_software_license_renewals | 'version': '18.0.1.0.0', |
| sf_spare_parts_minmax | 'version': '18.0.1.0.0', |
| sf_special_price_approval | 'version': '18.0.1.0.0', |
| sf_stock_adjustment_approval | 'version': '18.0.1.0.0', |
| sf_succession_plan | 'version': '18.0.1.0.0', |
| sf_supplier_audit_program | 'version': '18.0.1.0.0', |
| sf_supplier_audit_scheduler | 'version': '18.0.1.0.0', |
| sf_supplier_bank_change_alert | 'version': '18.0.1.0.0', |
| sf_supplier_capacity_check | 'version': '18.0.1.0.0', |
| sf_supplier_capacity_forecast | 'version': '18.0.1.0.0', |
| sf_supplier_capacity_planner | 'version': '18.0.1.0.0', |
| sf_supplier_capacity_review | 'version': '18.0.1.0.0', |
| sf_supplier_contract_database | 'version': '18.0.1.0.0', |
| sf_supplier_contract_renewal | 'version': '18.0.1.0.0', |
| sf_supplier_contract_renewal_alert | 'version': '18.0.1.0.0', |
| sf_supplier_contract_renewal_tracker | 'version': '18.0.1.0.0', |
| sf_supplier_diversity_tracker | 'version': '18.0.1.0.0', |
| sf_supplier_invoice_3way_match | 'version': '18.0.1.0.0', |
| sf_supplier_invoice_3way_match3 | 'version': '18.0.1.0.0', |
| sf_supplier_invoice_accuracy | 'version': '18.0.1.0.0', |
| sf_supplier_invoice_matching | 'version': '18.0.1.0.0', |
| sf_supplier_leadtime_audit | 'version': '18.0.1.0.0', |
| sf_supplier_negotiation_prep | 'version': '18.0.1.0.0', |
| sf_supplier_onboarding_checklist | 'version': '18.0.1.0.0', |
| sf_supplier_onboarding_portal | 'version': '18.0.1.0.0', |
| sf_supplier_pareto_abc | 'version': '18.0.1.0.0', |
| sf_supplier_payment_optimization | 'version': '18.0.1.0.0', |
| sf_supplier_payment_terms | 'version': '18.0.1.0.0', |
| sf_supplier_performance_dashboard | 'version': '18.0.1.0.0', |
| sf_supplier_performance_review | 'version': '18.0.1.0.0', |
| sf_supplier_pricing_benchmark | 'version': '18.0.1.0.0', |
| sf_supplier_pricing_history | 'version': '18.0.1.0.0', |
| sf_supplier_pricing_review | 'version': '18.0.1.0.0', |
| sf_supplier_pricing_tiers | 'version': '18.0.1.0.0', |
| sf_supplier_questionnaire | 'version': '18.0.1.0.0', |
| sf_supplier_risk_dashboard | 'version': '18.0.1.0.0', |
| sf_supplier_risk_mitigation | 'version': '18.0.1.0.0', |
| sf_supplier_risk_mitigation_plan | 'version': '18.0.1.0.0', |
| sf_supplier_risk_register | 'version': '18.0.1.0.0', |
| sf_supplier_risk_score | 'version': '18.0.1.0.0', |
| sf_supplier_scorecard_review | 'version': '18.0.1.0.0', |
| sf_system_health_check | 'version': '18.0.1.0.0', |
| sf_tax_deadline_calendar | 'version': '18.0.1.0.0', |
| sf_tax_provision_calc | 'version': '18.0.1.0.0', |
| sf_telework_policy | 'version': '18.0.1.0.0', |
| sf_territory_mapping | 'version': '18.0.1.0.0', |
| sf_third_party_risk | 'version': '18.0.1.0.0', |
| sf_tooling_request | 'version': '18.0.1.0.0', |
| sf_training_budget | 'version': '18.0.1.0.0', |
| sf_training_feedback | 'version': '18.0.1.0.0', |
| sf_treasury_week_board | 'version': '18.0.1.0.0', |
| sf_upsell_trigger_rules | 'version': '18.0.1.0.0', |
| sf_user_activity_log | 'version': '18.0.1.0.0', |
| sf_vendor_sample_tracking | 'version': '18.0.1.0.0', |
| sf_vendor_scorecard_auto | 'version': '18.0.1.0.0', |
| sf_vendor_sla_monitor | 'version': '18.0.1.0.0', |
| sf_warehouse_layout_planner | 'version': '18.0.1.0.0', |
| sf_warehouse_safety_log | 'version': '18.0.1.0.0', |
| sf_warehouse_slotting_review | 'version': '18.0.1.0.0', |
| sf_warehouse_throughput | 'version': '18.0.1.0.0', |
| sf_warehouse_throughput_daily | 'version': '18.0.1.0.0', |
| sf_warning_letter_register | 'version': '18.0.1.0.0', |
| sf_warranty_cost_analytics | 'version': '18.0.1.0.0', |
| sf_waste_stream_tracker | 'version': '18.0.1.0.0', |
| sf_win_loss_analysis | 'version': '18.0.1.0.0', |
| sf_workorder_handover | 'version': '18.0.1.0.0', |
| sf_zone_capacity_monitor | 'version': '18.0.1.0.0', |
